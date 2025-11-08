import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
GROUP_TOPIC_ID = int(os.getenv("GROUP_TOPIC_ID"))