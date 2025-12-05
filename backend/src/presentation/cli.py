import argparse
import sys
import os

from backend.src.core.analyzer import EmotionAnalyzer
from backend.src.infrastructure.logger import setup_logger
from backend.src.model.Input_data import InputData
from backend.src.core.detectors import DeepFaceEmotionDetector
from backend.src.infrastructure.storage import CSVStorage

# TODO: Change the hard-coded name to dynamic if possible
logger = setup_logger("cli.py")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Emotion Recognition Tool for Talk Show Analysis"
    )

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="Path to the input folder containing videos",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="./data/output",
        help="Path to save the output CSV/Excel files",
    ) 

    # TODO: Add command option for specifying the interval analyzing frames
    parser.add_argument(
        '--interval', 
        type=int, 
        default=1, 
        help="Analysis interval in seconds (default: Analyze 1 frame every second)"
    )

    parser.add_argument(
        "-m",
        "--image_path", 
        type=str,
        default="./data/input/img11.jpg",
        help="Path to the input image file",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    logger.info("Initializing Application...")

    # Select detector and storage implementations
    detector = DeepFaceEmotionDetector()
    storage = CSVStorage(output_path=args.output)

    # Wrap arguments in InputData dataclass
    input_data = InputData(
        image_path=args.image_path,
        video_path=args.input,
        output_path=args.output,
        interval=args.interval
    )

    # Initialize the main emotion analyzer
    analyzer = EmotionAnalyzer(input_data, detector=detector, storage=storage)
    analyzer.run()


if __name__ == "__main__":
    main()
