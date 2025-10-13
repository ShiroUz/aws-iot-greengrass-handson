import os
import logging

logger = logging.getLogger("FileUtil")

def save(file_path: str, data):
    """Save file"""
    try:
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'wb') as f:
            f.write(data)
        logger.debug(f"Successfully saved file to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save file to {file_path}: {str(e)}")
        return False

def read(file_name: str) -> str:
    """Read file"""
    try:
        with open(file_name, 'r') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Failed to read file {file_name}: {str(e)}")
        return None

def read_binary(file_name: str) -> bytes:
    """Read file in binary mode"""
    try:
        with open(file_name, 'rb') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Failed to read binary file {file_name}: {str(e)}")
        return None

def delete_file(file_path: str) -> bool:
    """Delete a file from the local system"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"Successfully deleted file: {file_path}")
            return True
        else:
            logger.warning(f"File does not exist: {file_path}")
            return False
    except Exception as e:
        logger.error(f"Failed to delete file {file_path}: {str(e)}")
        return False