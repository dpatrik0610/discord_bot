import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "/")
TEST_GUILD_ID= int(os.getenv("TEST_GUILD_ID", "0"))