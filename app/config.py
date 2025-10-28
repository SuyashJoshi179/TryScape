"""
TryScape - Configuration Module
Handles loading and managing application configuration from environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class."""
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '2025-04-01-preview')
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-image-1')
    AZURE_OPENAI_SORA_DEPLOYMENT_NAME = os.getenv('AZURE_OPENAI_SORA_DEPLOYMENT_NAME', 'sora')
    
    # Feature Flags
    ENABLE_SORA = os.getenv('ENABLE_SORA', 'false').lower() == 'true'
    
    # Flask Configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    # Host/Port for local development server
    FLASK_RUN_HOST = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    try:
        FLASK_RUN_PORT = int(os.getenv('FLASK_RUN_PORT', '5000'))
    except ValueError:
        FLASK_RUN_PORT = 5000
    
    # Upload Configuration
    UPLOAD_FOLDER = 'app/static/uploads'
    GENERATED_FOLDER = 'app/static/generated'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    @staticmethod
    def validate():
        """Validate that required configuration is present."""
        required_vars = [
            'AZURE_OPENAI_ENDPOINT',
            'AZURE_OPENAI_API_KEY',
        ]
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}. "
                f"Please check your .env file."
            )
