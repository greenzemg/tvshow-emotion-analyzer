import solara
import os
import solara
import os
import threading
import sys
import logging

from backend.src.application.analyzer import EmotionAnalyzer
from backend.src.application.stats import StatisticsService
from backend.src.domain.models import InputData
from backend.src.infrastructure.detectors import DeepFaceEmotionDetector
from backend.src.infrastructure.storage import CSVStorage
from backend.src.infrastructure.opencv_adapter import OpenCVVideoFactory

# REACTIVE STATE VARIABLES
# Configuration
input_path = solara.reactive("./data/input")
output_path = solara.reactive("./data/output")
frame_stride = solara.reactive(25)
detector_model = solara.reactive("DeepFace")

# Execution Status
is_processing = solara.reactive(False)
progress = solara.reactive(0)
status_message = solara.reactive("Ready")

# System Logs
logs = solara.reactive([])


# LOGIC / ACTIONS
def update_input_path(value):
    """Updates input path and verifies existence."""
    input_path.value = value
    # TODO: we could add validation logic here (e.g. check if valid dir)


def update_output_path(value):
    output_path.value = value


def reset_settings():
    frame_stride.value = 10
    input_path.value = "./data/inputs"
    output_path.value = "./data/outputs"


def add_log(message: str):
    """Helper to append log messages safely."""
    # Keep only the last 100 logs to prevent UI lag
    current = logs.value
    new_logs = current + [message]
    if len(new_logs) > 100:
        new_logs = new_logs[-100:]
    logs.value = new_logs


def _run_job():
    """Background task to run the analysis."""
    try:
        is_processing.value = True
        status_message.value = "Initializing AI Models..."
        logging.info("Starting Analysis Job...")

        # 1. Setup Infrastructure
        detector = DeepFaceEmotionDetector()
        storage = CSVStorage(output_path=output_path.value)
        video_factory = OpenCVVideoFactory()
        stats_service = StatisticsService(storage)

        input_data = InputData(
            video_path=input_path.value,
            output_path=output_path.value,
            interval=frame_stride.value,
        )

        # 2. Run Analyzer
        status_message.value = "Processing Videos..."
        analyzer = EmotionAnalyzer(input_data, detector, storage, video_factory)
        analyzer.run()

        # 3. Generate Stats
        status_message.value = "Generating Report..."
        stats_service.generate_report()

        status_message.value = "Analysis Complete!"
        logging.info("Job Finished Successfully.")

    except Exception as e:
        status_message.value = "Error Occurred"
        logging.error(f"Job Failed: {e}")
    finally:
        is_processing.value = False


def run_analysis_threaded():
    """Starts the analysis in a separate thread to keep UI responsive."""
    if is_processing.value:
        return

    thread = threading.Thread(target=_run_job)
    thread.start()
