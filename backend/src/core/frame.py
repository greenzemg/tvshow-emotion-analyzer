import os
import numpy as np

from backend.src.core.detectors import DeepFaceEmotionDetector
from backend.src.infrastructure.logger import setup_logger
from backend.src.model.output_data import OutputData

# Configure local logger
logger = setup_logger("core.frame.py")


class Frame:
    """Represents a single image or video frame.

    Attributes:
        image_path (str): Path to image file.
        image_data (np.ndarray): Raw image data.
        source_id (str): Identifier for the frame source.
        emotion_detector (DeepFaceEmotionDetector): Emotion detection service.
    """

    def __init__(
        self,
        image_path: str = None,
        image_data: np.ndarray = None,
        source_id: str = None,
        emotion_detector: DeepFaceEmotionDetector = DeepFaceEmotionDetector(),
    ):
        """Initialize a Frame instance.

        Args:
            image_path (str, optional): Path to image file.
            image_data (np.ndarray, optional): Raw image data.
            source_id (str, optional): Source identifier.
            emotion_detector (DeepFaceEmotionDetector, optional): Detector instance.

        Raises:
            ValueError: If neither image_path nor image_data is provided.
        """
        self.image_path = image_path
        self.image_data = image_data
        self.source_id = source_id
        self.emotion_detector = emotion_detector

        if not self.image_path and self.image_data is None:
            raise ValueError(
                "Frame must be initialized with either image_path or image_data"
            )

    def analyze(self):
        """Analyzes the frame for emotion.

        Returns:
            OutputData: Analysis result or None if failed.
        """
        target = self.image_path if self.image_path else self.image_data
        source_name = self.image_path if self.image_path else "InMemoryFrame"

        try:
            logger.debug(f"Analyzing frame: {source_name}")

            file_name = (
                os.path.basename(source_name) if self.image_path else self.source_id
            )
            results = self.emotion_detector.detect(target)

            output_data = OutputData(
                file_name=file_name,
                dominant_emotion=results.get("dominant_emotion"),
                emotion=results.get("emotion", {}),
            )

            return output_data

        except Exception as e:
            logger.error(f"Error analyzing {source_name}: {e}")
            return None
