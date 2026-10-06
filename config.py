import os
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.environ["AUTH0_DOMAIN"]
AUDIENCE = os.environ["AUTH0_AUDIENCE"]

# Default configuration for API calls (pre-filled in web form)
DEFAULT_API_URL = os.environ.get("DEFAULT_API_URL", "https://api.example.com")
DEFAULT_AUTH_TOKEN = os.environ.get("DEFAULT_AUTH_TOKEN", "")
DEFAULT_HEADERS = os.environ.get("DEFAULT_HEADERS", '{"Content-Type": "application/json"}')
