import argparse

from backend.src.application.analyzer import EmotionAnalyzer
from backend.src.application.stats import StatisticsService
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
    parser.add_argument('--interval', type=int, default=1, help="Frame extraction interval (process every Nth frame)")
    parser.add_argument('--no-report', action='store_true', help="Skip generation of summary report")
    return parser.parse_args()

def confirm_file_naming_convention():
    """
    Displays a visual guide for file naming and enforces user confirmation.
    """
    visual_guide = r"""
    +-------------------------------------------------------+
    |             Naming Convention of Video Files          |
    +-------------------------------------------------------+
    
    /data/input/{GuestName}/
    ├── GuestName_HostName_Topic.mp4
    ├── MarkRutte_MariekeElsinga_MSC.mkv
    └── MarkRutte_MatthijsNieuwkerk.mp4

    Format: Guest_Host_Topic.mp4
    """
    print(visual_guide)
    
    confirmation = input("Have you named your files accordingly? (y/n): ")
    if confirmation.lower() != 'y':
        logger.error("Please rename your files before proceeding.")
        exit(1)
        

def main():
    args = parse_arguments()

    # TODO: Ask for the user confirmation if the file are properly set
    # Also give an example how the video files should be named. E.g., showname_sXXeYY.mp4

    logger.info("Initializing Application...")

    confirm_file_naming_convention()

    # 1. Dependency Injection: Create Implementation instances (detector, storage, video factory)
    detector = DeepFaceEmotionDetector()
    storage = CSVStorage(output_path=args.output)
    video_factory = OpenCVVideoFactory()
    # Initialize Stats Service
    stats_service = StatisticsService(storage)

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
   
    # 3. Start excution of the pipelines 
    #                      +------------------------------+
    #  Video/Image --->    | Pipeline-1: Emotion Analysis | ---> Analysis Results
    #                      +------------------------------+
    analyzer = EmotionAnalyzer(input_data, detector=detector, storage=storage, video_factory=video_factory)
    analyzer.run()

    #                       +-------------------------------+
    #  Analysis Result ---> | Pipeline-2: Report Generation | --->  Statistical Report
    #                       +-------------------------------+
    if not args.no_report and args.video:
        stats_service.generate_report() 


if __name__ == "__main__":
    main()
