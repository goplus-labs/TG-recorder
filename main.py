from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
import config
import message_handler
import schedule
import time

# Set the id of group
SUMMARY_GROUP_ID = -1001826795915


async def send_daily_summary(client):
    today_messages = message_handler.get_today_messages()
    if not today_messages:
        summary = "Nothing happened today"
    else:
        summary = "Daily Security News：\n\n"
        for msg in today_messages:
            summary += f"{msg['date']} - {msg['user']}: {msg['text']}\n"
    await client.send_message(SUMMARY_GROUP_ID, summary)


async def main():
    async with TelegramClient(StringSession(config.SESSION_STRING), config.API_ID, config.API_HASH, proxy=config.PROXY) as client:
        client.add_event_handler(message_handler.handle_new_message, events.NewMessage())

        # add schedule task
        schedule.every().day.at("20:00").do(lambda: client.loop.create_task(send_daily_summary(client)))

        print("Bot is running. Press Ctrl+C to stop.")

        while True:
            schedule.run_pending()
            await asyncio.sleep(1)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
