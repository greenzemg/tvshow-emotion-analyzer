from pytest import param
from backend.src.model.Input_data import InputData
from backend.src.infrastructure.logger import setup_logger
from backend.src.core.detectors import IEmotionDetector
from backend.src.infrastructure.storage import IStorage
from backend.src.core.frame import Frame


logger = setup_logger("core.analyzer.py")


class EmotionAnalyzer:
    """An entry point for the emotion analysis process.

    Attributes:
        input_data (InputData): Configuration and input paths.
        detector (IEmotionDetector): Service for emotion detection.
        storage (IStorage): Service for saving results.
    """

    def __init__(
        self, input_data: InputData, detector: IEmotionDetector, storage: IStorage
    ):
        """Initializes the analyzer with dependencies."""
        self.input_data = input_data
        self.detector = detector
        self.storage = storage

    def run(self):
        """Executes the analysis workflow for images or videos."""
        logger.info(f"Starting analysis on {self.input_data.video_path}")

        try:
            if self.input_data.image_path:
                logger.info(f"Analyzing single image: {self.input_data.image_path}")
                # Step 1: Detect emotions in the image using frame object
                frame = Frame(
                    image_path=self.input_data.image_path,
                    emotion_detector=self.detector,
                )
                image_results = frame.analyze()
                # Step 2: Save the results
                self.storage.save(image_results)
            elif self.input_data.video_path:
                logger.info(
                    f"Analyzing videos in directory: {self.input_data.video_path}"
                )
            else:
                logger.error("No input image or video directory specified.")
                return
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
