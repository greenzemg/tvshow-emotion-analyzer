from typing import Any, Dict
from deepface import DeepFace

from backend.src.domain.interfaces import IEmotionDetector
from backend.src.infrastructure.logger import setup_logger

logger = setup_logger("core.detectors.py")


class DeepFaceEmotionDetector(IEmotionDetector):
    """Emotion detector implementation using the DeepFace library."""

    def detect(self, frame: Any) -> Dict[str, Any]:
        """Analyzes a single frame using DeepFace.

        Args:
            frame (Any): File path (str) or image array (numpy.ndarray).

        Returns:
            Dict[str, Any]: Detection results or None if failed.
        """
        try:
            # DeepFace.analyze supports both paths and numpy arrays
            # Hence, frame could be either a file path or image data
            results = DeepFace.analyze(
                img_path=frame,
                actions=["emotion"],
                enforce_detection=True,
                detector_backend="opencv",  # fast backend for video processing
            )

            if not results:
                return None

            # Take the first face found
            first_face = results[0]

            return first_face

        except ValueError:
            # Expected error when no face is found
            return None
        except Exception as e:
            logger.error(f"Error analyzing frame using deepface: {e}")
            return None
