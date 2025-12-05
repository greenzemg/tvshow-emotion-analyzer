import cv2
import os
import logging
from typing import Optional
import numpy as np
from backend.src.domain.interfaces import IVideoSource, IVideoFactory

logger = logging.getLogger("OpenCVAdapter")

class OpenCVVideoSource(IVideoSource):
    """
    Concrete implementation of IVideoSource using OpenCV.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.cap = None

    def open(self) -> bool:
        if not os.path.exists(self.file_path):
            logger.error(f"File not found: {self.file_path}")
            return False
        
        self.cap = cv2.VideoCapture(self.file_path)
        if not self.cap.isOpened():
            logger.error(f"Failed to open video: {self.file_path}")
            return False
        return True

    def get_fps(self) -> float:
        if self.cap and self.cap.isOpened():
            return self.cap.get(cv2.CAP_PROP_FPS)
        return 0.0

    def read(self) -> Optional[np.ndarray]:
        if not self.cap or not self.cap.isOpened():
            return None
        
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self) -> None:
        if self.cap:
            self.cap.release()

class OpenCVVideoFactory(IVideoFactory):
    """
    Factory to create OpenCVVideoSource instances.
    """
    def create(self, file_path: str) -> IVideoSource:
        return OpenCVVideoSource(file_path)