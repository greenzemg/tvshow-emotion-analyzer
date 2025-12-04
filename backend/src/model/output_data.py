from dataclasses import dataclass
from typing import Dict


@dataclass
class OutputData:
    """
    Data class model for storing image/video analysis result.
    """

    file_name: str
    dominant_emotion: str
    emotion: Dict[str, float]
