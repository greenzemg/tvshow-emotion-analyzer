from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class InputData:
    """
    Data class model for storing command line input parameters.
    """

    image_path: Optional[str] = None
    video_path: Optional[str] = None
    output_path: str = "./data/output"
    interval: float = 1.0 # Process one frame seconsds


@dataclass
class OutputData:
    """
    Data class model for storing image/video analysis result.
    """

    file_name: str
    dominant_emotion: str
    emotion: Dict[str, float]
    timestamp: str = "00:00"  # timestamp field to handle video timeline

@dataclass
class VideoStats:
    """
    Data class for statistical summary of a single video.
    """
    file_name: str
    total_frames: int
    most_frequent_emotion: str
    emotion_distribution: Dict[str, float] # e.g., {'happy': 40.0, 'sad': 10.0}
