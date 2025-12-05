from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import numpy as np
from backend.src.domain.models import OutputData


class IStorage(ABC):
    """Abstract interface for data storage."""

    @abstractmethod
    def save(self, data: OutputData) -> None:
        """Saves analysis data to storage."""
        pass

    @abstractmethod
    def write_batch(self, rows: list[OutputData]) -> None:
        """Writes a batch of data."""
        pass


class IEmotionDetector(ABC):
    """Abstract interface for emotion detection strategies."""

    @abstractmethod
    def detect(self, frame: Any) -> Optional[Dict[str, Any]]:
        """
        Detects emotion in a given image (path or numpy array).
        Returns raw result dictionary or None.
        """
        pass

class IVideoSource(ABC):
    """
    Abstract interface for reading frames from a video source.
    """
    @abstractmethod
    def open(self) -> bool:
        """Prepares the video source for reading."""
        pass

    @abstractmethod
    def get_fps(self) -> float:
        """Returns the frames per second of the source."""
        pass

    @abstractmethod
    def read(self) -> Optional[np.ndarray]:
        """Reads the next frame. Returns None if end of stream."""
        pass

    @abstractmethod
    def release(self) -> None:
        """Releases resources."""
        pass

class IVideoFactory(ABC):
    """Factory interface to create video sources from paths."""
    @abstractmethod
    def create(self, file_path: str) -> IVideoSource:
        pass