# Records everything your system does — for debugging, monitoring, and auditing.

#So you get:
# 1. Time-stamped logs
# 2. Log levels (INFO, WARNING, ERROR)
# 3. Saved to a file

# What It Logs

# 1.Pipeline start/stop
# 2.Data ingestion success/failure
# 3.Model accuracy
# 4.Errors and exceptions

# This file sets up logging for your project.
# Logging means keeping a record of what your system is doing.
# This helps in debugging, monitoring, and checking errors later.

import logging  
import os       
from datetime import datetime  

# Create a log file name using the current date and time
# Example: 01_18_2026_10_30_45.log
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


# Create a folder named "logs" in the current working directory
LOGS_PATH = os.path.join(os.getcwd(), "logs")

# Make sure the folder exists, if not, create it
os.makedirs(LOGS_PATH, exist_ok=True)


# Create the full path for the log file inside the logs folder
LOG_FILE_PATH = os.path.join(LOGS_PATH, LOG_FILE)


# Configure the logging system
logging.basicConfig(
    filename=LOG_FILE_PATH,  # Where the log file will be saved
    format="[ %(asctime)s ] %(levelname)s - %(message)s",  # Log format
    level=logging.INFO,  # Log only INFO level and above (INFO, WARNING, ERROR)
)


# Create a logger object with a custom name
# You will use this in other files like:
# logger.info("This is an info message")
# logger.error("This is an error message")
logger = logging.getLogger("mlproject_logger")
