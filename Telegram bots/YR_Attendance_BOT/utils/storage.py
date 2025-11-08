import json
from pathlib import Path

FILE_PATH = Path("chat_ids.json")

async def load_chat_ids():
    if FILE_PATH.exists():
        return json.loads(FILE_PATH.read_text())
    return []

async def save_chat_id(chat_id):
    chat_ids = await load_chat_ids()
    if str(chat_id) not in chat_ids:
        chat_id = str(chat_id)
        if chat_id.startswith("-"):
            chat_ids.append(chat_id)
            FILE_PATH.write_text(json.dumps(chat_ids))
