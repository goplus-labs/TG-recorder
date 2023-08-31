from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
import config
import message_handler
import schedule
import openai
from config import OPENAI_API_KEY, SUMMARY_GROUP_ID
import time
import json


def remove_first_last_two_lines(s):
    lines = s.splitlines()
    return '\n'.join(lines[0:-1])


async def send_daily_summary(client):
    all_messages = message_handler.get_today_messages()
    print(all_messages)
    messages_text = '\n'.join([msg['text'] for msg in all_messages])
    print(messages_text)
    messages_str = json.dumps(all_messages, indent=2)
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a very knowledgeable assistant in web3 and security."},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": f"We are a media focused on Web3 Security. I would like you to \
                help me summarize all the messages from a Telegram group called ETHSecurity Community, extract and \
                refine information related to Web3 security, filter out irrelevant information, and create a daily \
                report without emphasizing the speaker's information. Below is the JSON of the messages I crawled\
                :{messages_str}, I would like the output to look something like this: 🚀2023-08-31\nNEAR has gotten \
                some nice criticals with their program \n2. xxx \n3. xxx"},
            {"role": "user", "content": f"{messages_str}"}
        ]
    )

    summary = response.choices[0].message.content.strip()
    summary = remove_first_last_two_lines(summary)

    await client.send_message(SUMMARY_GROUP_ID, summary)


async def main():
    async with TelegramClient(StringSession(config.SESSION_STRING), config.API_ID, config.API_HASH) as client:
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
