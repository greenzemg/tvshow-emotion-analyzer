import os
import logging


def setup_logger(name="EmotionTool", log_file="./log/app.log", level=logging.INFO):
    """
    Sets up a standard logger to output to console.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    
     # Prevent adding duplicate handlers if logger is already set up
    if logger.handlers:
        return logger

    # 1. Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - [%(name)s] - %(levelname)s - %(message)s"
    )

    # 2. Console Handler (StreamHandler defaults to stderr, which is safer)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 3. File Handler (Optional)
    if log_file:
        # Ensure directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        

    return logger
