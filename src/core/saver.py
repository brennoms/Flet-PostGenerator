import os
import re
from PIL import Image
from src.core.config_manager import ConfigManager

class PostSaver:
    """
    Handles saving generated images to the file system with 
    smart folder organization.
    """

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """Removes characters that aren't allowed in filenames."""
        return re.sub(r'[\\/*?:"<>|]', "", filename).strip().replace(" ", "-").lower()

    @classmethod
    def save_post(cls, images: list[Image.Image], base_path: str, post_name: str) -> str:
        """
        Saves images. If one image, saves as file. 
        If multiple, creates a folder.
        Returns the path where it was saved.
        """
        clean_name = cls._sanitize_filename(post_name)
        
        # Ensure the base directory exists
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        # CASE 1: Single Image
        if len(images) == 1:
            save_path = os.path.join(base_path, f"{clean_name}.png")
            images[0].save(save_path, "PNG")
            return save_path

        # CASE 2: Multiple Images (Carousel)
        else:
            folder_path = os.path.join(base_path, clean_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            for i, img in enumerate(images, start=1):
                img_path = os.path.join(folder_path, f"{i}.png")
                img.save(img_path, "PNG")
            
            return folder_path

class DirectoryNotFoundError(Exception):
    pass

def save_post_in_default_directory(images: list[Image.Image], post_name: str) -> str:
    config_manager = ConfigManager()
    config = config_manager.load()

    if not config.working_directory:
        raise DirectoryNotFoundError("No working directory defined in settings.")

    if not os.path.exists(config.working_directory):
        raise DirectoryNotFoundError(f"The directory '{config.working_directory}' does not exist.")

    return PostSaver.save_post(images, config.working_directory, post_name)
