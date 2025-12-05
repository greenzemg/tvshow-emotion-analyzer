import argparse
import sys
import os

from backend.src.application.analyzer import EmotionAnalyzer
from backend.src.infrastructure.logger import setup_logger
from backend.src.domain.models import InputData
from backend.src.infrastructure.detectors import DeepFaceEmotionDetector
from backend.src.infrastructure.storage import CSVStorage
from backend.src.infrastructure.opencv_adapter import OpenCVVideoFactory

# TODO: Change the hard-coded name to dynamic if possible
logger = setup_logger("cli.py")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Emotion Recognition Tool for Talk Show Analysis")
    parser.add_argument('-i', '--image', type=str, help="Path to a single image file")
    parser.add_argument('-v', '--video', type=str, help="Path to a video file or folder")
    parser.add_argument('-o', '--output', type=str, default='./data/output', help="Path to save analysis results")
    parser.add_argument('--interval', type=int, default=1, help="Analysis interval in seconds (default: Analyze 1 frame every second)")
    return parser.parse_args()


def main():
    args = parse_arguments()

    logger.info("Initializing Application...")

    # 1. Dependency Injection: Create Implementation instances (detector, storage, video factory)
    detector = DeepFaceEmotionDetector()
    storage = CSVStorage(output_path=args.output)
    video_factory = OpenCVVideoFactory()

    # 2. Wrap arguments in InputData dataclass
    input_data = InputData(
        image_path=args.image,
        video_path=args.video,
        output_path=args.output,
        interval=args.interval,
    )

    if not input_data.image_path and not input_data.video_path:
        logger.error("You must provide either --image or --video input.")
        return
    
    # 3. Initialize the main emotion analyzer with all dependencies
    analyzer = EmotionAnalyzer(input_data, detector=detector, storage=storage, video_factory=video_factory)

    # 4. Run 
    analyzer.run()


if __name__ == "__main__":
    main()
