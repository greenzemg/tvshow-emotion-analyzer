import csv
import os
from typing import Any, Dict, List

from backend.src.domain.interfaces import IStorage
from backend.src.domain.models import OutputData
from backend.src.domain.models import VideoStats
from backend.src.infrastructure.logger import setup_logger

logger = setup_logger("CSVStorage")


class CSVStorage(IStorage):
    """Handles writing analysis results to a CSV file."""

    def __init__(self, output_path: str):
        """Initializes storage with output directory."""
        self.output_path = output_path

        # Check if directory exists
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path, exist_ok=True)

        self.raw_csv_path = os.path.join(self.output_path, "analysis_results.csv")
        self.stats_csv_path = os.path.join(self.output_path, "summary_report.csv")

        self.fieldnames = [
            'file_name', 'timestamp', 'dominant_emotion', 'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise',
            'neutral'
        ]

        self.stats_fieldnames = [
            "file_name", "total_frames", "most_frequent_emotion", "pct_happy", "pct_sad", "pct_angry", "pct_neutral",
            "pct_fear", "pct_surprise", "pct_disgust"
        ]

    def save(self, data: OutputData):
        """Appends a single analysis result to the CSV."""
        csv_row = {
            "file_name": data.file_name,
            "timestamp": data.timestamp,
            "dominant_emotion": data.dominant_emotion,
            "angry": data.emotion.get("angry", 0),
            "disgust": data.emotion.get("disgust", 0),
            "fear": data.emotion.get("fear", 0),
            "happy": data.emotion.get("happy", 0),
            "sad": data.emotion.get("sad", 0),
            "surprise": data.emotion.get("surprise", 0),
            "neutral": data.emotion.get("neutral", 0),
        }

        self._write_to_file(csv_row)

    def load_all(self) -> List[Dict[str, Any]]:
        """Reads the raw CSV file back into memory."""
        if not os.path.exists(self.raw_csv_path):
            logger.warning("No analysis results found to load.")
            return []

        data = []
        try:
            with open(self.raw_csv_path, mode="r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data.append(row)
        except Exception as e:
            logger.error(f"Error reading CSV: {e}")
        return data

    def save_stats(self, stats_list: List[VideoStats]):
        """Writes the summary report."""
        try:
            with open(self.stats_csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.stats_fieldnames)
                writer.writeheader()

                for stat in stats_list:
                    # Flatten the dictionary for CSV
                    row = {
                        "file_name": stat.file_name,
                        "total_frames": stat.total_frames,
                        "most_frequent_emotion": stat.most_frequent_emotion,
                        "pct_happy": stat.emotion_distribution.get("happy", 0),
                        "pct_sad": stat.emotion_distribution.get("sad", 0),
                        "pct_angry": stat.emotion_distribution.get("angry", 0),
                        "pct_neutral": stat.emotion_distribution.get("neutral", 0),
                        "pct_fear": stat.emotion_distribution.get("fear", 0),
                        "pct_surprise": stat.emotion_distribution.get("surprise", 0),
                        "pct_disgust": stat.emotion_distribution.get("disgust", 0),
                    }
                    writer.writerow(row)
            logger.info(f"Statistics report saved to {self.stats_csv_path}")
        except Exception as e:
            logger.error(f"Error saving stats: {e}")

    def _map_model_to_row(self, data: OutputData) -> dict:
        return {
            "file_name": data.file_name,
            "timestamp": data.timestamp,
            "dominant_emotion": data.dominant_emotion,
            "angry": data.emotion.get("angry", 0),
            "disgust": data.emotion.get("disgust", 0),
            "fear": data.emotion.get("fear", 0),
            "happy": data.emotion.get("happy", 0),
            "sad": data.emotion.get("sad", 0),
            "surprise": data.emotion.get("surprise", 0),
            "neutral": data.emotion.get("neutral", 0),
        }

    def _write_to_file(self, row: dict):
        """Writes a dictionary row to the CSV file."""
        file_exists = os.path.isfile(self.raw_csv_path)
        try:
            with open(self.raw_csv_path, mode="a", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(row)
        except Exception as e:
            logger.error(f"Error writing to CSV: {e}")

    def write_batch(self, rows: List[OutputData]) -> None:
        """Writes a list of rows to the CSV."""
        for row in rows:
            self.save(row)
