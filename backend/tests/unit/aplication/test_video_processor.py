from backend.src.application.video import Video
from backend.tests.conftest import MockEmotionDetector
from backend.tests.conftest import MockVideoSource


def test_process_every_frame():
    """Test that stride=1 processes all frames."""
    source = MockVideoSource(num_frames=10, fps=1.0)  # 10 seconds, 10 frames
    detector = MockEmotionDetector()
    video = Video(source, detector, "test.mp4")

    # Run processing
    results = list(video.process(frame_step=1))

    assert len(results) == 10
    assert results[0].timestamp == "00:00"
    assert results[9].timestamp == "00:09"


def test_process_with_stride():
    """Test that stride=2 skips every other frame."""
    source = MockVideoSource(num_frames=10, fps=1.0)
    detector = MockEmotionDetector()
    video = Video(source, detector, "test.mp4")

    # Run processing with stride 2
    results = list(video.process(frame_step=2))

    # Should process frames 0, 2, 4, 6, 8 (Total 5)
    assert len(results) == 5
    assert results[0].timestamp == "00:00"
    assert results[1].timestamp == "00:02"


def test_handles_empty_video():
    """Test that processor handles empty streams gracefully."""
    source = MockVideoSource(num_frames=0)
    detector = MockEmotionDetector()
    video = Video(source, detector, "test.mp4")

    results = list(video.process(frame_step=1))
    assert len(results) == 0


def test_stress_large_video_stream():
    """
    STRESS TEST: Large Volume.
    Process a video with 10,000 frames to ensure the generator doesn't hang 
    or consume excessive memory (logic check).
    """
    # 10,000 frames at 30 FPS
    source = MockVideoSource(num_frames=10000, fps=30.0)
    detector = MockEmotionDetector()
    video = Video(source, detector, "large.mp4")

    # Process every 100th frame
    results = list(video.process(frame_step=100))

    # Expect 100 results (0, 100, 200, ..., 9900)
    assert len(results) == 100
    assert results[-1].timestamp == "05:30"  # 9900/30 = 330s = 5m 30s


def test_stress_invalid_fps():
    """
    STRESS TEST: Robustness (Division by Zero).
    Video source reports 0 FPS (e.g., corrupt header).
    Should handle gracefully without crashing.
    """
    source = MockVideoSource(num_frames=100, fps=0.0)
    detector = MockEmotionDetector()
    video = Video(source, detector, "corrupt_fps.mp4")

    # Should log error and return empty generator
    results = list(video.process(frame_step=1))
    assert len(results) == 0


def test_stress_negative_stride():
    """
    STRESS TEST: Robustness (Input Validation).
    User provides negative stride. Logic should clamp to 1.
    """
    source = MockVideoSource(num_frames=5, fps=30.0)
    detector = MockEmotionDetector()
    video = Video(source, detector, "test.mp4")

    # Stride -5 should be treated as 1 (or max(1, -5))
    results = list(video.process(frame_step=-5))
    assert len(results) == 5


def test_stress_stride_larger_than_video():
    """
    STRESS TEST: Edge Case.
    Stride is 100, but video only has 10 frames.
    Should process the first frame (idx 0) and then finish.
    """
    source = MockVideoSource(num_frames=10, fps=30.0)
    detector = MockEmotionDetector()
    video = Video(source, detector, "short.mp4")

    results = list(video.process(frame_step=100))

    # 0 % 100 == 0 -> Process
    # Next check is 100, which is > 9 -> Stop
    assert len(results) == 1
    assert results[0].timestamp == "00:00"
