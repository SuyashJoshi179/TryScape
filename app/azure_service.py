"""
TryScape - Azure OpenAI Service
Handles integration with Azure OpenAI API for image generation.
"""
import os
import requests
from typing import Optional
from openai import AzureOpenAI
from app.config import Config
from PIL import Image
import uuid
import base64


class AzureOpenAIService:
    """Service class for Azure OpenAI image generation."""
    
    def __init__(self):
        """Initialize Azure OpenAI client."""
        self.client = AzureOpenAI(
            api_version=Config.AZURE_OPENAI_API_VERSION,
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            api_key=Config.AZURE_OPENAI_API_KEY,
        )
        self.deployment_name = Config.AZURE_OPENAI_DEPLOYMENT_NAME
        self.sora_deployment_name = Config.AZURE_OPENAI_SORA_DEPLOYMENT_NAME
    
    def generate_tryscape_image(
        self,
        user_image_path: str,
        user_description: str,
        clothing_description: str,
        location_description: str,
        style: str = "photorealistic"
    ) -> Optional[str]:
        """
        Generate a photorealistic image using Azure OpenAI gpt-image-1 (image editing).
        
        Args:
            user_image_path: Path to the user's uploaded image
            user_description: Description of the user's appearance
            clothing_description: Description of the clothing items
            location_description: Description of the location
            style: Image style (default: photorealistic)
        
        Returns:
            URL of the generated image or None if generation fails
        """
        # Construct detailed prompt for image editing
        prompt = self._construct_prompt(
            user_description,
            clothing_description,
            location_description,
            style
        )
        
        # If we're running in debug mode, avoid calling Azure and return
        # a local placeholder image URL so the rest of the pipeline can be exercised.
        if getattr(Config, 'DEBUG', False):
            try:
                os.makedirs(Config.GENERATED_FOLDER, exist_ok=True)
                placeholder = Image.new('RGB', (1024, 1024), color=(200, 200, 200))
                filename = f"mock_generated_{uuid.uuid4().hex}.png"
                filepath = os.path.join(Config.GENERATED_FOLDER, filename)
                placeholder.save(filepath, format='PNG')
                host = getattr(Config, 'FLASK_RUN_HOST', '127.0.0.1')
                port = getattr(Config, 'FLASK_RUN_PORT', 5000)
                return f"http://{host}:{port}/static/generated/{filename}"
            except Exception as e:
                print(f"Error creating mock image: {e}")
                return None

        try:
            # Create a mask for the entire image (edit everything)
            # For image editing API, we need both the original image and a mask
            mask_path = self._create_full_mask(user_image_path)
            
            # Use REST API since OpenAI SDK may not support image editing yet
            endpoint = Config.AZURE_OPENAI_ENDPOINT.rstrip('/')
            url = f"{endpoint}/openai/deployments/{self.deployment_name}/images/edits?api-version={Config.AZURE_OPENAI_API_VERSION}"
            
            headers = {
                'Authorization': f'Bearer {Config.AZURE_OPENAI_API_KEY}'
            }
            
            # Prepare files for multipart upload
            with open(user_image_path, 'rb') as img_file, open(mask_path, 'rb') as mask_file:
                files = {
                    'image': ('image.png', img_file, 'image/png'),
                    'mask': ('mask.png', mask_file, 'image/png'),
                }
                data = {
                    'prompt': prompt
                }
                
                print(f"Sending image edit request to gpt-image-1...")
                print(f"URL: {url}")
                print(f"Prompt: {prompt[:100]}...")
                
                response = requests.post(url, headers=headers, files=files, data=data, timeout=120)
                
                print(f"Response status: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"Error response: {response.text}")
                    return None
                
                result = response.json()
            
            # Clean up mask file
            try:
                os.remove(mask_path)
            except Exception:
                pass
            
            # Extract the base64 image from response
            if 'data' in result and len(result['data']) > 0:
                first_result = result['data'][0]
                
                # Handle base64-encoded image
                if 'b64_json' in first_result:
                    try:
                        image_bytes = base64.b64decode(first_result['b64_json'])
                        os.makedirs(Config.GENERATED_FOLDER, exist_ok=True)
                        filename = f"generated_{uuid.uuid4().hex}.png"
                        save_path = os.path.join(Config.GENERATED_FOLDER, filename)
                        with open(save_path, 'wb') as f:
                            f.write(image_bytes)
                        host = getattr(Config, 'FLASK_RUN_HOST', '127.0.0.1')
                        port = getattr(Config, 'FLASK_RUN_PORT', 5000)
                        return f"http://{host}:{port}/static/generated/{filename}"
                    except Exception as e:
                        print(f"Error saving base64 image: {e}")
                        return None
                
                # Handle URL response
                if 'url' in first_result:
                    return first_result['url']
            
            print("Image editing returned no usable image data:", result)
            return None

        except Exception as e:
            print(f"Error generating image: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _create_full_mask(self, image_path: str) -> str:
        """
        Create a full white mask for the image (indicating entire image should be edited).
        
        Args:
            image_path: Path to the source image
            
        Returns:
            Path to the generated mask file
        """
        try:
            # Open the source image to get dimensions
            with Image.open(image_path) as img:
                # Convert to RGBA if not already
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Create a white mask (fully transparent in alpha = edit everywhere)
                # For gpt-image-1, white areas indicate where to edit
                mask = Image.new('RGBA', img.size, (255, 255, 255, 255))
                
                # Save mask
                mask_filename = f"mask_{uuid.uuid4().hex}.png"
                mask_path = os.path.join(Config.UPLOAD_FOLDER, mask_filename)
                mask.save(mask_path, 'PNG')
                
                return mask_path
        except Exception as e:
            print(f"Error creating mask: {e}")
            # Return a default mask if creation fails
            mask = Image.new('RGBA', (1024, 1024), (255, 255, 255, 255))
            mask_path = os.path.join(Config.UPLOAD_FOLDER, f"mask_default_{uuid.uuid4().hex}.png")
            mask.save(mask_path, 'PNG')
            return mask_path
    
    def _construct_prompt(
        self,
        user_description: str,
        clothing_description: str,
        location_description: str,
        style: str
    ) -> str:
        """
        Construct a detailed prompt for image generation.
        
        Args:
            user_description: Description of the user
            clothing_description: Description of clothing
            location_description: Description of location
            style: Image style
        
        Returns:
            Constructed prompt string
        """
        prompt = f"""Create a {style} image of a person with the following characteristics:

Person: {user_description}

Wearing: {clothing_description}

Location: {location_description}

The image should be high-quality, {style}, and show the person naturally posed in the location wearing the described outfit. The lighting and atmosphere should match the location."""
        
        return prompt
    
    def download_image(self, image_url: str, save_path: str) -> bool:
        """
        Download generated image from URL and save to local path.
        
        Args:
            image_url: URL of the image to download
            save_path: Local path to save the image
        
        Returns:
            True if successful, False otherwise
        """
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            return True
            
        except Exception as e:
            print(f"Error downloading image: {e}")
            return False
    
    def generate_tryscape_video(
        self,
        user_description: str,
        clothing_description: str,
        location_description: str,
        style: str = "photorealistic"
    ) -> Optional[str]:
        """
        Generate a video using Azure OpenAI SORA.
        
        Args:
            user_description: Description of the user's appearance
            clothing_description: Description of the clothing items
            location_description: Description of the location
            style: Video style (default: photorealistic)
        
        Returns:
            URL of the generated video or None if generation fails
        """
        # Construct detailed prompt for SORA
        prompt = self._construct_prompt(
            user_description,
            clothing_description,
            location_description,
            style
        )
        
        # If we're running in debug mode, return a placeholder
        if getattr(Config, 'DEBUG', False):
            return "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
        
        try:
            import time
            import requests as req
            
            # SORA uses REST API with job-based async pattern
            # Endpoint: POST {endpoint}/openai/v1/video/generations/jobs?api-version=preview
            headers = {
                'api-key': Config.AZURE_OPENAI_API_KEY,
                'Content-Type': 'application/json'
            }
            
            # Create video generation job
            endpoint = Config.AZURE_OPENAI_ENDPOINT.rstrip('/')
            create_url = f"{endpoint}/openai/v1/video/generations/jobs?api-version=preview"
            
            payload = {
                "prompt": prompt
            }
            
            print(f"Creating SORA video generation job...")
            print(f"Endpoint: {create_url}")
            print(f"Payload: {payload}")
            
            create_response = req.post(create_url, headers=headers, json=payload, timeout=30)
            
            # Log response for debugging
            print(f"SORA API Response Status: {create_response.status_code}")
            print(f"SORA API Response Body: {create_response.text}")
            
            if create_response.status_code != 200:
                print(f"SORA API Error: {create_response.text}")
                return None
            
            job_data = create_response.json()
            
            job_id = job_data.get('id')
            if not job_id:
                print(f"No job ID in response: {job_data}")
                return None
            
            print(f"Video generation job created: {job_id}")
            
            # Poll for job completion (timeout after 5 minutes)
            max_wait = 300  # 5 minutes
            poll_interval = 5  # 5 seconds
            elapsed = 0
            
            status_url = f"{endpoint}/openai/v1/video/generations/jobs/{job_id}?api-version=preview"
            
            while elapsed < max_wait:
                time.sleep(poll_interval)
                elapsed += poll_interval
                
                # Check job status
                status_response = req.get(status_url, headers=headers, timeout=30)
                status_response.raise_for_status()
                status_data = status_response.json()
                
                status = status_data.get('status')
                print(f"Video generation status: {status} (elapsed: {elapsed}s)")
                
                if status == "succeeded":
                    # Get the video URL
                    output = status_data.get('output', {})
                    video_url = output.get('url') if isinstance(output, dict) else None
                    
                    if video_url:
                        # Download and save the video
                        try:
                            os.makedirs(Config.GENERATED_FOLDER, exist_ok=True)
                            filename = f"generated_{uuid.uuid4().hex}.mp4"
                            save_path = os.path.join(Config.GENERATED_FOLDER, filename)
                            
                            if self.download_image(video_url, save_path):  # Reuse download method
                                host = getattr(Config, 'FLASK_RUN_HOST', '127.0.0.1')
                                port = getattr(Config, 'FLASK_RUN_PORT', 5000)
                                return f"http://{host}:{port}/static/generated/{filename}"
                            else:
                                return video_url  # Return Azure URL if download fails
                        except Exception as e:
                            print(f"Error downloading video: {e}")
                            return video_url  # Return Azure URL as fallback
                    else:
                        print(f"Video generation succeeded but no URL found in output: {output}")
                        return None
                
                elif status == "failed":
                    error = status_data.get('error', 'Unknown error')
                    print(f"Video generation failed: {error}")
                    return None
                
                elif status in ["notStarted", "running"]:
                    # Continue polling
                    continue
                else:
                    print(f"Unknown status: {status}")
                    return None
            
            print(f"Video generation timed out after {max_wait} seconds")
            return None
            
        except Exception as e:
            print(f"Error generating video: {e}")
            import traceback
            traceback.print_exc()
            return None

