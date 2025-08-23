# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

API_BASE_URL = "https://api.spacetraders.io/v2"
API_TOKEN = os.getenv("SPACETRADERS_TOKEN")

if not API_TOKEN:
    raise ValueError(
        "Missing API token. Please set SPACETRADERS_TOKEN in your environment or .env file."
    )

# (Optional) other config
REQUEST_TIMEOUT = 10  # seconds
