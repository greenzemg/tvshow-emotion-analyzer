import os

from backend.src.application.frame import Frame
from backend.src.application.video import Video
from backend.src.domain.interfaces import IEmotionDetector
from backend.src.domain.interfaces import IStorage
from backend.src.domain.interfaces import IVideoFactory
from backend.src.domain.models import InputData
from backend.src.domain.models import OutputData

# TODO: We have dependency here from application to infrastructure layer. Fix it.
from backend.src.infrastructure.file_utils import FileUtils
from backend.src.infrastructure.logger import setup_logger

# TODO: Analzyer is dependent on infrastructure layer. It should depend on domain (interfaces) only.
logger = setup_logger("core.analyzer.py")


class EmotionAnalyzer:
    """An entry point for the emotion analysis process.

    Attributes:
        input_data (InputData): Configuration and input paths.
        detector (IEmotionDetector): Service for emotion detection.
        storage (IStorage): Service for saving results.
    """

    def __init__(
        self,
        input_data: InputData,
        detector: IEmotionDetector,
        storage: IStorage,
        video_factory: IVideoFactory,
    ):
        """Initializes the analyzer with dependencies."""
        self.input_data = input_data
        self.detector = detector
        self.storage = storage
        self.video_factory = video_factory

    def run(self):
        """Executes the analysis workflow for images or videos."""
        logger.info(f"Starting analysis on {self.input_data.video_path}")

        try:
            if self.input_data.image_path:
                self._process_image(self.input_data.image_path)
            elif self.input_data.video_path:
                if os.path.isdir(self.input_data.video_path):
                    self._process_directory(self.input_data.video_path)
                else:
                    self._process_video(self.input_data.video_path)
            else:
                logger.error("No input image or video directory specified.")
                return
        except Exception as e:
            logger.error(f"Error during analysis: {e}")

    def _process_image(self, image_path: str):

        logger.info(f"Analyzing single image: {image_path}")
        try:
            filename = os.path.basename(image_path)

            frame = Frame(
                image_path=image_path,
                source_id=filename,
                emotion_detector=self.detector,
            )
            # 1. Detect emotions in the image using frame object
            result: OutputData = frame.analyze()

            if result:
                # 2. Save the results
                self.storage.save(result)
                logger.info(f"Finished image: {filename}")
            else:
                logger.warning(f"No face detected in image: {filename}")

        except Exception as e:
            logger.error(f"Failed to process image {image_path}: {e}")

    def _process_video(self, video_path: str):
        logger.info(f"Analyzing video: {video_path}")

        try:
            # 1. Using factory to create the infrastructure implementation (Source)
            source = self.video_factory.create(video_path)
            source_id = os.path.basename(video_path)

            # 2. Inject source into the logic (Video)
            video = Video(source, self.detector, source_id)

            results_generator = video.process(frame_step=self.input_data.interval)

            batch_buffer = []
            for result in results_generator:
                batch_buffer.append(result)
                if len(batch_buffer) >= 10:
                    self.storage.write_batch(batch_buffer)
                    batch_buffer = []

            if batch_buffer:
                self.storage.write_batch(batch_buffer)

        except Exception as e:
            logger.error(f"Failed to process video {video_path}: {e}")

    def _process_directory(self, directory: str):
        logger.info(f"Analyzing videos in directory: {self.input_data.video_path}")

        try:
            videos = FileUtils.get_video_files(directory)
        except FileNotFoundError as e:
            logger.error(str(e))
            return

        logger.info(f"Found {len(videos)} videos in {directory}")
        for video_path in videos:
            self._process_video(video_path)
