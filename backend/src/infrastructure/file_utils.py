import os
from typing import List

from backend.src.infrastructure.logger import setup_logger

logger = setup_logger("core.analyzer.py")

class FileUtils:
    @staticmethod
    def get_possible_dirs():
        """
        Get a list of possible directories where files might be located.
        Returns:
            List[str]: A list of directory paths.
        """
        base_dir = os.path.dirname(__file__)
        return [
            os.path.join(base_dir, "../../data/out"),
            os.path.join(base_dir, "../../data/in"),
        ]

    @staticmethod
    def get_video_files(directory: str) -> List[str]:
        """
        Scans a directory and returns a list of video file paths.
        Supports common video extensions.
        """
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv'}
        video_files = []

        logger.info(f"Getting video from folder")

        if not os.path.exists(directory):
            raise FileNotFoundError(f"Input directory not found: {directory}")

        for root, _, files in os.walk(directory):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in video_extensions:
                    video_files.append(os.path.join(root, file))

        logger.debug(f"video files {video_files}")

        return video_files
        
