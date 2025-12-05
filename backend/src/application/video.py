from typing import Generator

from backend.src.application.analyzer import Frame
from backend.src.domain.interfaces import IEmotionDetector, IVideoSource
from backend.src.domain.models import OutputData
from backend.src.infrastructure.logger import setup_logger

logger = setup_logger("VideoProcessor")


class Video:
    """
    Contain a logic for processing a video stream.
    It models the real world video item with added behavior
    """

    def __init__(
        self, source: IVideoSource, detector: IEmotionDetector, source_id: str
    ):
        """
        Args:
            source: The interface to read frames.
            detector: The interface to analyze emotions.
            source_id: The identifier (filename) for reporting.
        """
        self.source = source
        self.detector = detector
        self.source_id = source_id

    def process(self, interval_seconds: int = 1) -> Generator[OutputData, None, None]:
        """
        Process for frame extraction and analysis.
        """
        if not self.source.open():
            logger.error(f"Could not open source: {self.source_id}")
            return

        fps = self.source.get_fps()
        if fps <= 0:
            logger.error(f"Invalid FPS ({fps}) for source: {self.source_id}")
            self.source.release()
            return

        # frame_interval = int(fps * interval_seconds)
        frame_interval = max(1, interval_seconds)
        current_frame_idx = 0
        processed_count = 0

        logger.info(f"Starting processing: {self.source_id} (FPS: {fps:.2f})")

        try:
            while True:
                frame_data = self.source.read()
                if frame_data is None:
                    break  # End of stream

                if current_frame_idx % frame_interval == 0:
                    # Inject detector into Frame
                    frame_obj = Frame(
                        image_data=frame_data,
                        source_id=self.source_id,
                        emotion_detector=self.detector,
                    )

                    result: OutputData = frame_obj.analyze()

                    # Results are yielded one by one for efficiency
                    if result:
                        result.timestamp = self._frame_to_time(current_frame_idx, fps)
                        yield result
                        processed_count += 1

                    if processed_count % 10 == 0 and processed_count > 0:
                        logger.info(f"Processed {processed_count} frames...")

                current_frame_idx += 1
        finally:
            self.source.release()
            logger.info(
                f"Finished {self.source_id}. Total detections: {processed_count}"
            )

    def _frame_to_time(self, frame_idx: int, fps: float) -> str:
        seconds = int(frame_idx / fps)
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"
