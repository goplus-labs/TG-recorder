from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import config

with TelegramClient(StringSession(), config.API_ID, config.API_HASH, proxy=config.PROXY) as client:
    print("Session string:", client.session.save())
