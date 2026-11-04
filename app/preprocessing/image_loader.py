"""preprocessing .py : This module helps to load an image ."""

import cv2 
from pathlib import Path


class Loader:

    def __init__(self, image_path):
        self.image_path = Path(image_path)
        self.image = None

    def load_image(self):
        """Reads and returns an image"""
        # Check whether the image exists
        if not self.image_path.exists():
            raise FileNotFoundError(f"Image not found: {self.image_path}")

        # Check whether the path is a file
        if not self.image_path.is_file():
            raise ValueError("Provided path is not a file.")

        # Load the image
        self.image = cv2.imread(str(self.image_path))

        # Check whether OpenCV loaded the image
        if self.image is None:
            raise ValueError("Could not load image. The file may be corrupted or unsupported.")
        
        return self.image
    
    def info(self):
        """Returns height, width and color channels of an image."""

        if self.image is None:
            raise ValueError("Load an image before requesting its information.")

        height, width, channels = self.image.shape
        
        return height, width, channels
