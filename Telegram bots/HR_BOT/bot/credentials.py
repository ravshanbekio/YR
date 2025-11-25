import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")