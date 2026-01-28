from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
ADMIN_IDS = set(map(int, os.getenv("ADMIN_IDS", "").split(",")))