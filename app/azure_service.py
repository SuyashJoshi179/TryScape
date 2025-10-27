"""
TryScape - Azure OpenAI Service
Handles integration with Azure OpenAI API for image generation.
"""
import os
import requests
from typing import Optional
from openai import AzureOpenAI
from app.config import Config


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
    
    def generate_tryscape_image(
        self,
        user_description: str,
        clothing_description: str,
        location_description: str,
        style: str = "photorealistic"
    ) -> Optional[str]:
        """
        Generate a photorealistic image using Azure OpenAI DALL-E 3.
        
        Args:
            user_description: Description of the user's appearance
            clothing_description: Description of the clothing items
            location_description: Description of the location
            style: Image style (default: photorealistic)
        
        Returns:
            URL of the generated image or None if generation fails
        """
        # Construct detailed prompt for DALL-E 3
        prompt = self._construct_prompt(
            user_description,
            clothing_description,
            location_description,
            style
        )
        
        try:
            response = self.client.images.generate(
                model=self.deployment_name,
                prompt=prompt,
                n=1,
                size="1024x1024",
                quality="hd",
                style="natural"
            )
            
            if response.data and len(response.data) > 0:
                return response.data[0].url
            return None
            
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
    
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
