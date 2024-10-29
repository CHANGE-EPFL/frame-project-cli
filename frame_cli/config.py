import os

from dotenv import load_dotenv

load_dotenv()

LOGGING_LEVEL = os.getenv("FRAME_CLI_LOGGING_LEVEL", "INFO")
