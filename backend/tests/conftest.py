from typing import Any, Dict, List, Optional

import numpy as np
import pytest

from backend.src.domain.interfaces import IEmotionDetector
from backend.src.domain.interfaces import IStorage
from backend.src.domain.interfaces import IVideoSource
from backend.src.domain.models import OutputData
from backend.src.domain.models import VideoStats


# -------------------------------------------
# MOCKS
# -------------------------------------------
class MockVideoSource(IVideoSource):
    """Simulates a video stream without using OpenCV."""

    def __init__(self, num_frames=30, fps=30.0):
        self.num_frames = num_frames
        self._fps = fps
        self.current_idx = 0
        self.is_opened = True

    def open(self) -> bool:
        return self.is_opened  # type: ignore

    def get_fps(self) -> float:
        return self._fps  # type: ignore

    def read(self) -> Optional[np.ndarray]:
        if self.current_idx >= self.num_frames:
            return None
        self.current_idx += 1
        # Return a fake black 100x100 image
        return np.zeros((100, 100, 3), dtype=np.uint8)  # type: ignore

    def release(self) -> None:
        self.is_opened = False


class MockStorage(IStorage):
    """Stores data in memory lists instead of CSV files."""

    def __init__(self):
        self.saved_data: List[OutputData] = []
        self.saved_stats: List[VideoStats] = []

    def save(self, data: OutputData) -> None:
        self.saved_data.append(data)

    def write_batch(self, rows: list[OutputData]) -> None:
        self.saved_data.extend(rows)

    def load_all(self) -> List[Dict[str, Any]]:
        # Convert objects back to dicts to simulate reading from CSV
        return [{
            "file_name": d.file_name,
            "dominant_emotion": d.dominant_emotion,
            "timestamp": d.timestamp,
        } for d in self.saved_data]

    def save_stats(self, stats: List[VideoStats]) -> None:
        self.saved_stats.extend(stats)


class MockEmotionDetector(IEmotionDetector):
    """Returns a deterministic emotion."""

    def __init__(self, fixed_emotion="happy"):
        self.fixed_emotion = fixed_emotion

    def detect(self, image: Any) -> Optional[Dict[str, Any]]:
        # Always return the fixed emotion with 100% confidence
        return {
            "dominant_emotion": self.fixed_emotion,
            "emotion": {
                self.fixed_emotion: 100.0
            },
        }


# -------------------------------------------
# FIXTURES
# -------------------------------------------
@pytest.fixture
def mock_video_source():
    return MockVideoSource(num_frames=100, fps=30.0)


@pytest.fixture
def mock_storage():
    return MockStorage()


@pytest.fixture
def mock_detector():
    return MockEmotionDetector(fixed_emotion="happy")
