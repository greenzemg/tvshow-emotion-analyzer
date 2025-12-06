from backend.src.application.stats import StatisticsService
from backend.src.domain.models import OutputData


def test_generate_report_calculates_correct_percentages(mock_storage):
    """Test that correct percentages are calculated for a single video."""
    service = StatisticsService(mock_storage)

    # 1. Setup Data: 6 Happy, 4 Sad frames for "video1.mp4"
    data = []
    for _ in range(6):
        data.append(OutputData("video1.mp4", "happy", {}, "00:00"))
    for _ in range(4):
        data.append(OutputData("video1.mp4", "sad", {}, "00:00"))

    mock_storage.write_batch(data)

    # 2. Run Service
    service.generate_report()

    # 3. Verify Results
    assert len(mock_storage.saved_stats) == 1
    stats = mock_storage.saved_stats[0]

    assert stats.file_name == "video1.mp4"
    assert stats.total_frames == 10
    assert stats.most_frequent_emotion == "happy"
    assert stats.emotion_distribution["happy"] == 60.0
    assert stats.emotion_distribution["sad"] == 40.0


def test_generate_report_multiple_videos(mock_storage):
    """Test grouping logic for multiple videos."""
    service = StatisticsService(mock_storage)

    data = [
        OutputData("videoA.mp4", "happy", {}, "00:00"),
        OutputData("videoB.mp4", "sad", {}, "00:00"),
    ]
    mock_storage.write_batch(data)

    service.generate_report()

    assert len(mock_storage.saved_stats) == 2
    filenames = {s.file_name for s in mock_storage.saved_stats}
    assert "videoA.mp4" in filenames
    assert "videoB.mp4" in filenames


def test_stress_large_dataset(mock_storage):
    """
    STRESS TEST: Large Volume.
    Verify the service handles a large number of frames (e.g., 10,000) 
    without crashing or calculation errors.
    """
    service = StatisticsService(mock_storage)

    # Generate 10,000 frames (50% happy, 50% sad)
    # This ensures the logic scales beyond trivial examples
    large_batch = []
    for i in range(5000):
        large_batch.append(OutputData("long_video.mp4", "happy", {}, "00:00"))
        large_batch.append(OutputData("long_video.mp4", "sad", {}, "00:00"))

    mock_storage.write_batch(large_batch)

    service.generate_report()

    assert len(mock_storage.saved_stats) == 1
    stats = mock_storage.saved_stats[0]

    assert stats.total_frames == 10000
    # Floating point math should be reasonably close
    assert stats.emotion_distribution['happy'] == 50.0
    assert stats.emotion_distribution['sad'] == 50.0


def test_stress_empty_storage(mock_storage):
    """
    STRESS TEST: Empty Input.
    The service should not crash if the input CSV is empty or non-existent.
    """
    service = StatisticsService(mock_storage)

    # Do not write any data to storage
    # Run Service
    service.generate_report()

    # Should exit gracefully and produce no stats
    assert len(mock_storage.saved_stats) == 0


def test_stress_corrupt_data_rows(mock_storage):
    """
    STRESS TEST: Dirty Data.
    Simulate rows where 'dominant_emotion' might be missing or None 
    (e.g., from a failed API call).
    """
    service = StatisticsService(mock_storage)

    data = [
        OutputData("video1.mp4", "happy", {}, "00:00"),
        # Corrupt row: emotion is None or empty string
        OutputData("video1.mp4", "", {}, "00:00"),
        OutputData("video1.mp4", None, {}, "00:00")
    ]
    mock_storage.write_batch(data)

    service.generate_report()

    stats = mock_storage.saved_stats[0]
    # Should only count the 1 valid row, ignoring the 2 corrupt ones
    assert stats.total_frames == 1
    assert stats.most_frequent_emotion == "happy"


def test_stress_tie_breaking(mock_storage):
    """
    STRESS TEST: Edge Case (Tie).
    Ensure deterministic behavior when two emotions have equal counts.
    """
    service = StatisticsService(mock_storage)

    data = [OutputData("tie.mp4", "happy", {}, "00:00"), OutputData("tie.mp4", "sad", {}, "00:00")]
    mock_storage.write_batch(data)

    service.generate_report()

    stats = mock_storage.saved_stats[0]
    assert stats.total_frames == 2
    # Counter.most_common() preserves insertion order for ties,
    # so "happy" should win because it was added first.
    assert stats.most_frequent_emotion == "happy"
