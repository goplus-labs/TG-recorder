import datetime
import json
from config import SUMMARY_GROUP_ID
from telethon.utils import get_display_name

from main import send_daily_summary

TARGET_GROUP_ID = -1001372269197


def load_messages_from_file():
    try:
        with open('messages.json', 'r') as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

all_messages = load_messages_from_file()


def save_messages_to_file():
    with open('messages.json', 'w') as f:
        json.dump(all_messages, f)


def get_today_messages():
    today = datetime.date.today()
    today_messages = [msg for msg in all_messages if datetime.datetime.fromisoformat(msg['date']).date() == today]
    return today_messages


async def handle_new_message(event):
    if event.is_group and event.chat_id == TARGET_GROUP_ID:
        sender = await event.get_sender()
        message_data = {
            'date': str(event.date),
            'user': sender.first_name,
            'text': event.text
        }
        all_messages.append(message_data)
        save_messages_to_file()

    if event.is_group and event.chat_id == SUMMARY_GROUP_ID:
        if "Daily Report" in event.raw_text and event.mentioned:
            await send_daily_summary(event.client)


