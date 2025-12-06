from typing import List, Dict, Counter
from backend.src.domain.models import VideoStats
from backend.src.domain.interfaces import IStorage
from backend.src.infrastructure.logger import setup_logger

logger = setup_logger("StatsService")


class StatisticsService:
    """
    Read raw analysis data and generating a statistical summary.
    """

    def __init__(self, storage: IStorage):
        self.storage = storage

    def generate_report(self):
        """
        Reads all raw data, aggregates by video file, and saves the summary.
        """
        logger.info("Generating statistical report...")

        # 1. Load Data
        raw_rows = self.storage.load_all()
        if not raw_rows:
            logger.warning("No data found to generate report.")
            return

        # 2. Group by Video
        # structure: {'video_name': [list of dominant emotions]}
        video_groups: Dict[str, List[str]] = {}

        for row in raw_rows:
            filename = row.get("file_name")
            emotion = row.get("dominant_emotion")

            if filename and emotion:
                if filename not in video_groups:
                    video_groups[filename] = []
                video_groups[filename].append(emotion)

        # 3. Calculate Stats for each video
        stats_list: List[VideoStats] = []

        for filename, emotions in video_groups.items():
            total = len(emotions)
            counts = Counter(emotions)

            # Find winner
            most_frequent = counts.most_common(1)[0][0]

            # Calculate percentages
            distribution = {
                emotion: round((count / total) * 100, 2)
                for emotion, count in counts.items()
            }

            stats = VideoStats(
                file_name=filename,
                total_frames=total,
                most_frequent_emotion=most_frequent,
                emotion_distribution=distribution,
            )
            stats_list.append(stats)

        # 4. Save Report
        self.storage.save_stats(stats_list)
        logger.info(f"Report generated for {len(stats_list)} videos.")
