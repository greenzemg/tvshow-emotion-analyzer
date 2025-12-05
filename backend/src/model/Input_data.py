from dataclasses import dataclass


@dataclass
class InputData:
    """
    Data class model for storing command line input parameters.
    """
    image_path: str
    video_path: str
    output_path: str
    interval: int = 1 