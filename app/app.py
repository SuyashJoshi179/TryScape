"""
TryScape - Main Application Module
Flask web application for TryScape image generation.
"""
from flask import Flask, render_template, request, jsonify, url_for
import os
import uuid
from datetime import datetime

from app.config import Config
from app.azure_service import AzureOpenAIService
from app.utils.image_utils import ImageProcessor
from app.utils.file_utils import allowed_file, save_uploaded_file


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure required directories exist
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.GENERATED_FOLDER, exist_ok=True)
    
    # Initialize services
    azure_service = AzureOpenAIService()
    image_processor = ImageProcessor()
    
    @app.route('/')
    def index():
        """Render the main page."""
        return render_template('index.html', enable_sora=Config.ENABLE_SORA)
    
    @app.route('/generate', methods=['POST'])
    def generate_image():
        """
        Handle image generation request.
        
        Expected form data:
        - user_image: Image file of the user
        - clothing_image: Image file of clothing (optional)
        - user_description: Text description of user
        - clothing_description: Text description of clothing
        - location_description: Text description or name of location
        """
        try:
            # Validate request
            if 'user_image' not in request.files:
                return jsonify({'error': 'No user image provided'}), 400
            
            user_image = request.files['user_image']
            
            if user_image.filename == '':
                return jsonify({'error': 'No user image selected'}), 400
            
            if not allowed_file(user_image.filename):
                return jsonify({'error': 'Invalid file type for user image'}), 400
            
            # Save uploaded user image
            user_image_path = save_uploaded_file(
                user_image, 
                Config.UPLOAD_FOLDER, 
                prefix='user_'
            )
            
            # Validate and resize image
            if not image_processor.validate_image(user_image_path):
                os.remove(user_image_path)
                return jsonify({'error': 'Invalid user image file'}), 400
            
            image_processor.resize_image(user_image_path)
            
            # Process clothing image if provided
            clothing_image_path = None
            if 'clothing_image' in request.files:
                clothing_image = request.files['clothing_image']
                if clothing_image.filename != '' and allowed_file(clothing_image.filename):
                    clothing_image_path = save_uploaded_file(
                        clothing_image,
                        Config.UPLOAD_FOLDER,
                        prefix='clothing_'
                    )
                    if image_processor.validate_image(clothing_image_path):
                        image_processor.resize_image(clothing_image_path)
                    else:
                        os.remove(clothing_image_path)
                        clothing_image_path = None
            
            # Get text descriptions
            user_description = request.form.get('user_description', 'a person')
            clothing_description = request.form.get('clothing_description', 'casual outfit')
            location_description = request.form.get('location_description', 'outdoor setting')
            generation_type = request.form.get('generation_type', 'image')  # 'image' or 'video'
            
            # Check if SORA is enabled when video is requested
            if generation_type == 'video' and not Config.ENABLE_SORA:
                return jsonify({'error': 'Video generation is not enabled'}), 400
            
            # Generate image or video using Azure OpenAI
            if generation_type == 'video':
                media_url = azure_service.generate_tryscape_video(
                    user_description=user_description,
                    clothing_description=clothing_description,
                    location_description=location_description
                )
                file_extension = 'mp4'
            else:
                media_url = azure_service.generate_tryscape_image(
                    user_image_path=user_image_path,  # Pass the uploaded image path
                    user_description=user_description,
                    clothing_description=clothing_description,
                    location_description=location_description
                )
                file_extension = 'png'
            
            if not media_url:
                return jsonify({'error': 'Failed to generate ' + generation_type}), 500
            
            # Download generated media
            generated_filename = f"generated_{uuid.uuid4().hex}.{file_extension}"
            generated_path = os.path.join(Config.GENERATED_FOLDER, generated_filename)
            
            if not azure_service.download_image(media_url, generated_path):
                return jsonify({'error': 'Failed to download generated ' + generation_type}), 500
            
            # Return success response
            return jsonify({
                'success': True,
                'generated_media_url': url_for('static', filename=f'generated/{generated_filename}'),
                'media_type': generation_type,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            print(f"Error in generate_image: {e}")
            # Don't expose internal error details to users
            return jsonify({'error': 'An error occurred while generating the image. Please try again.'}), 500
    
    @app.route('/health')
    def health():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'service': 'TryScape',
            'timestamp': datetime.now().isoformat()
        })
    
    return app


if __name__ == '__main__':
    try:
        Config.validate()
        app = create_app()
        # Use Config-host/port so `.env` can override defaults
        host = getattr(Config, 'FLASK_RUN_HOST', '0.0.0.0')
        port = getattr(Config, 'FLASK_RUN_PORT', 5000)
        app.run(host=host, port=port, debug=Config.DEBUG)
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please ensure all required environment variables are set in .env file")
