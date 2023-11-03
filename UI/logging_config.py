import logging

# Configure the logger
logging.basicConfig(
    filename="app.log",  # The name of the log file
    level=logging.INFO,  # The log level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # The format of the log message
)

logger = logging.getLogger(__name__)