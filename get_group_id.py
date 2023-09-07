from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import config


async def list_groups(client):
    for dialog in await client.get_dialogs():
        if dialog.is_group:
            print(f"Group name: {dialog.name}. ID: {dialog.id}")


with TelegramClient(StringSession(config.SESSION_STRING), config.API_ID, config.API_HASH, proxy=config.PROXY) as client:
    if not client.is_user_authorized():
        client.send_code_request(config.PHONE_NUMBER)
        client.sign_in(config.PHONE_NUMBER, input('Enter the code: '))

    client.loop.run_until_complete(list_groups(client))
