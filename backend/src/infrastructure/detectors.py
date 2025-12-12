from typing import Any, Dict, List, Optional

from deepface import DeepFace
import numpy as np

from backend.src.domain.interfaces import IEmotionDetector
from backend.src.infrastructure.logger import setup_logger

logger = setup_logger("core.detectors.py")


class DeepFaceEmotionDetector(IEmotionDetector):
    """Emotion detector implementation using the DeepFace library."""

    def __init__(self, model_name: str = "VGG-Face", distance_metric: str = "cosine"):
        self.model_name = model_name
        self.distance_metric = distance_metric
        # Thresholds vary by model/metric.
        # For VGG-Face + Cosine, 0.40 is the standard recommended threshold.
        self.threshold = 0.40

    def detect(self, image: Any, reference_embedding: Optional[List[float]] = None) -> Optional[Dict[str, Any]]:
        """
        Detects emotion. If reference_embedding is provided, it filters for that specific person.
        """
        try:
            # Analyze ALL faces in the frame (enforce_detection=False handles empty frames gracefully)
            results = DeepFace.analyze(
                img_path=image,
                actions=["emotion"],
                enforce_detection=False,
                detector_backend="opencv",
                silent=True,
            )

            if not results:
                return None

            # Scenario A: No Target (Default) -> Return Dominant Face (first one)
            if reference_embedding is None:
                result = results[0]
                return {
                    "dominant_emotion": result["dominant_emotion"],
                    "emotion": result["emotion"],
                }

            # Scenario B: Guest Targeting -> Find the face that matches
            for res in results:
                region = res["region"]
                x, y, w, h = region["x"], region["y"], region["w"], region["h"]

                # Crop the face from the original image for verification
                # Ensure coordinates are within bounds
                h_img, w_img, _ = image.shape
                x = max(0, x)
                y = max(0, y)
                w = min(w, w_img - x)
                h = min(h, h_img - y)

                face_crop = image[y:y + h, x:x + w]

                # Check if this face matches the Guest
                if self.verify(face_crop, reference_embedding):
                    # Found the guest! Return their emotion.
                    return {
                        "dominant_emotion": res["dominant_emotion"],
                        "emotion": res["emotion"],
                    }

            # If we looped through all faces and found no match, return None
            return None

        except Exception as e:
            logger.error(f"Emotion detection failed: {e}")
            return None

    def generate_embedding(self, image_path: str) -> Optional[List[float]]:
        """
        Calculates the facial embedding vector for the reference image.
        Returns None if no face is found in the reference photo.
        """
        try:
            logger.info(f"Generating embedding for reference: {image_path}")
            embedding_objs = DeepFace.represent(
                img_path=image_path, model_name=self.model_name, enforce_detection=True, detector_backend='opencv'
            )

            if not embedding_objs:
                logger.error("No face detected in reference image!")
                return None

            # Return the embedding vector of the first face found
            return list(embedding_objs[0]["embedding"])

        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            return None

    def verify(self, face_image: Any, reference_embedding: List[float]) -> bool:
        """
        Checks if the face in 'face_image' matches the 'reference_embedding'.
        Uses Cosine Distance manually for speed.
        """
        try:
            # 1. Get embedding for the current face
            # We disable enforce_detection because the face is passed directly from the VideoProcessor
            target_objs = DeepFace.represent(
                img_path=face_image,
                model_name=self.model_name,
                enforce_detection=False,
                detector_backend='skip'  # Optimization: image is already cropped/detected
            )

            if not target_objs:
                return False

            target_embedding = target_objs[0]["embedding"]

            # 2. Calculate Cosine Distance
            # Distance = 1 - Cosine Similarity
            a = np.array(reference_embedding)
            b = np.array(target_embedding)

            # Avoid division by zero
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)
            if norm_a == 0 or norm_b == 0:
                return False

            cosine_similarity = np.dot(a, b) / (norm_a * norm_b)
            cosine_distance = 1 - cosine_similarity

            # 3. Compare with Threshold
            is_match = cosine_distance < self.threshold
            return bool(is_match)

        except Exception as e:
            logger.warning(f"Verification failed: {e}")
            return False
