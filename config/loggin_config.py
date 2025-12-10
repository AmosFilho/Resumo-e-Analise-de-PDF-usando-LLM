import logging

# Create or get the logger
logger = logging.getLogger('shared_logger')
logger.setLevel(logging.DEBUG)  # Log everything (DEBUG level or higher)

# Prevent multiple handlers if the logger is configured multiple times
if not logger.handlers:
    # Create a file handler to log to a file
    file_handler = logging.FileHandler('utils/shared_log_file.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Define log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add file handler to logger
    logger.addHandler(file_handler)