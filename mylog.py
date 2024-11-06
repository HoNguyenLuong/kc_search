import logging

logging.basicConfig(
    filename='error_log.txt',   # Name of the file where logs will be saved
    filemode='a',               # Append mode; use 'w' to overwrite
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
)