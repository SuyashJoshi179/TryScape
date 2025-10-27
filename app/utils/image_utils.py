"""
TryScape - Image Processing Utilities
Utilities for processing and analyzing uploaded images.
"""
import base64
from PIL import Image
from io import BytesIO
from typing import Tuple, Optional


class ImageProcessor:
    """Utility class for image processing operations."""
    
    @staticmethod
    def validate_image(file_path: str) -> bool:
        """
        Validate that a file is a valid image.
        
        Args:
            file_path: Path to the image file
        
        Returns:
            True if valid image, False otherwise
        """
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_image_dimensions(file_path: str) -> Optional[Tuple[int, int]]:
        """
        Get dimensions of an image.
        
        Args:
            file_path: Path to the image file
        
        Returns:
            Tuple of (width, height) or None if error
        """
        try:
            with Image.open(file_path) as img:
                return img.size
        except Exception:
            return None
    
    @staticmethod
    def resize_image(file_path: str, max_size: int = 1024) -> bool:
        """
        Resize image to fit within max_size while maintaining aspect ratio.
        
        Args:
            file_path: Path to the image file
            max_size: Maximum dimension size
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with Image.open(file_path) as img:
                # Convert to RGB if necessary
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                # Calculate new size maintaining aspect ratio
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # Save resized image
                img.save(file_path, quality=95, optimize=True)
            return True
        except Exception as e:
            print(f"Error resizing image: {e}")
            return False
    
    @staticmethod
    def image_to_base64(file_path: str) -> Optional[str]:
        """
        Convert image to base64 string.
        
        Args:
            file_path: Path to the image file
        
        Returns:
            Base64 encoded string or None if error
        """
        try:
            with open(file_path, 'rb') as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except Exception:
            return None
    
    @staticmethod
    def describe_image_basic(file_path: str) -> str:
        """
        Generate a basic description of an image based on its properties.
        
        Args:
            file_path: Path to the image file
        
        Returns:
            Basic description string
        """
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                mode = img.mode
                format_name = img.format or 'unknown'
                
                return f"Image: {width}x{height}, {mode} mode, {format_name} format"
        except Exception:
            return "Unable to analyze image"
