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
    interval: int = 1


@dataclass
class OutputData:
    """
    Data class model for storing image/video analysis result.
    """

    file_name: str
    dominant_emotion: str
    emotion: Dict[str, float]
    timestamp: str = "00:00"  # timestamp field to handle video timeline
