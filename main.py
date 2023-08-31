from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
import config
import message_handler
import schedule
import openai
from config import OPENAI_API_KEY, SUMMARY_GROUP_ID
import time


async def send_daily_summary(client):
    all_messages = message_handler.get_today_messages()
    print(all_messages)
    messages_text = '\n'.join([msg['text'] for msg in all_messages])
    print(messages_text)
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Summarize today's group chat:\n\n{messages_text}\n\nSummary, and make it into a daily report using bulletlist"
    )

    summary = response.choices[0].text.strip()

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
