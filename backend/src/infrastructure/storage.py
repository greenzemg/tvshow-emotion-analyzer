from typing import Dict, List
import csv
import os

from backend.src.infrastructure.logger import setup_logger
from backend.src.domain.models import OutputData
from backend.src.domain.interfaces import IStorage

logger = setup_logger("CSVStorage")


class CSVStorage(IStorage):
    """Handles writing analysis results to a CSV file."""

    def __init__(self, output_path: str):
        """Initializes storage with output directory."""
        self.output_path = output_path
        
        # Check if directory exists
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path, exist_ok=True)
            
        self.csv_path = os.path.join(self.output_path, "analysis_results.csv")

        self.fieldnames = [
            'file_name', 'timestamp', 'dominant_emotion', 
            'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'
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

    def _write_to_file(self, row: dict):
        """Writes a dictionary row to the CSV file."""
        file_exists = os.path.isfile(self.csv_path)
        try:
            with open(self.csv_path, mode="a", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(row)
        except Exception as e:
            logger.error(f"Error writing to CSV: {e}")

    def write_batch(self, rows: List[Dict]):
        """Writes a list of rows to the CSV."""
        for row in rows:
            self.save(row)
