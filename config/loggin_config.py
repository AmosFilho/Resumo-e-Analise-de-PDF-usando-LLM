import logging
import os

# Ensure the directory for logs exists BEFORE creating FileHandler
# This prevents FileNotFoundError when the logger initializes
log_dir = "utils"
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "shared_log_file.log")

# Create or get the logger instance
logger = logging.getLogger('shared_logger')

# Set the lowest level to capture all logs (DEBUG and above)
logger.setLevel(logging.DEBUG)

# Prevent adding duplicate handlers if this file is imported multiple times
if not logger.handlers:
    # FileHandler writes logs into a file
    # 'encoding=utf-8' avoids Unicode errors in logs
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Define how each log line should look
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Attach the formatter to the handler
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)
