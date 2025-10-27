"""
TryScape - File Handling Utilities
Utilities for managing file uploads and storage.
"""
import os
import uuid
from werkzeug.utils import secure_filename
from app.config import Config


def allowed_file(filename: str) -> bool:
    """
    Check if a file has an allowed extension.
    
    Args:
        filename: Name of the file to check
    
    Returns:
        True if file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def save_uploaded_file(file, folder: str, prefix: str = "") -> str:
    """
    Save an uploaded file with a unique filename.
    
    Args:
        file: FileStorage object from Flask
        folder: Folder to save the file in
        prefix: Optional prefix for the filename
    
    Returns:
        Path to the saved file
    """
    # Generate unique filename
    original_filename = secure_filename(file.filename)
    extension = original_filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{prefix}{uuid.uuid4().hex}.{extension}"
    
    # Ensure folder exists
    os.makedirs(folder, exist_ok=True)
    
    # Save file
    file_path = os.path.join(folder, unique_filename)
    file.save(file_path)
    
    return file_path


def cleanup_old_files(folder: str, max_age_hours: int = 24) -> int:
    """
    Remove files older than max_age_hours from a folder.
    
    Args:
        folder: Folder to clean up
        max_age_hours: Maximum age in hours
    
    Returns:
        Number of files removed
    """
    import time
    
    if not os.path.exists(folder):
        return 0
    
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    removed_count = 0
    
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                try:
                    os.remove(file_path)
                    removed_count += 1
                except Exception as e:
                    print(f"Error removing {file_path}: {e}")
    
    return removed_count
