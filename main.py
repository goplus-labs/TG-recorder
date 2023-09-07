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


def split_long_message(message, max_length=4096):
    return [message[i:i+max_length] for i in range(0, len(message), max_length)]


def remove_first_last_two_lines(s):
    lines = s.splitlines()
    if "🚀" not in lines[0]:
        return '\n'.join(lines[1:-1])
    else:
        return '\n'.join(lines[0:-1])


async def send_daily_summary(client):
    chinese_summary_prompt = f"你是一个中文的群聊总结的助手，你可以为一个telegram的群聊记录，提取并总结每个时间段大家在重点讨论的话题内容。\
                请帮我将给出的群聊内容总结成一个今日的群聊报告，包含不多于10个的话题的总结（如果还有更多话题，可以在后面简单补充）。每个话题包含以下内容：\
                - 话题名(50字以内，带序号1️⃣2️⃣3️⃣，同时附带热度，以🔥数量表示）\n\
                - 参与者(不超过5个人，将重复的人名去重) \n\
                - 时间段(从几点到几点) \n\
                - 过程(50到200字左右）\n\
                - 评价(50字以下) \n\
                - 分割线： ------------ \n\
                另外有以下要求：\
                1. 每个话题结束使用 ------------ 分割 \
                2. 使用中文冒号 \
                3. 整段总结的大标题为 📰[当日日期]Daily Report \
                4. 总结内容得是中文 \
                以下是群聊内容:"
    english_summary_prompt = f"You are an assistant for summarizing group chats. \
    You can record, extract, and summarize the topics discussed by everyone in a \
    Telegram group chat during each time period. Please help me summarize today's \
    group chat content into a report containing no more than 10 topics (if there are \
    more topics, you can briefly add them later). Each topic includes the following \
    information: \
    - Topic name (within 50 characters, with a number 1️⃣2️⃣3️⃣, and accompanied by popularity represented by the number of 🔥) \
    - Participants (no more than 5 people, and duplicate names should be removed) \
    - Time period (from what time to what time) \
    - Process (about 50 to 200 words) \
    - Evaluation (within 50 words) \
    - Divider: ------------ \
    In addition, the following requirements should be met: \
    1. Use a divider of ------------ at the end of each topic \
    2. The main title of the entire summary should be 📰[Today's Date] Daily Report \
    3. The summary content should be in English \
    Here is the group chat content:"
    all_messages = message_handler.get_today_messages()
    messages_text = '\n'.join([msg['text'] for msg in all_messages])
    messages_str = json.dumps(all_messages, indent=2)
    openai.api_key = OPENAI_API_KEY
    response_cn = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages= [
            {"role": "assistant", "content": chinese_summary_prompt},
            {"role": "user", "content": f"{messages_str}"}
        ]
    )
    # response_en = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo-16k",
    #     messages=[
    #         {"role": "assistant", "content": english_summary_prompt},
    #         {"role": "user", "content": f"{messages_str}"}
    #     ]
    # )

    summary_cn = response_cn.choices[0].message.content.strip()
    # summary_en = response_en.choices[0].message.content.strip()
    summaries_cn = split_long_message(summary_cn)
    # summaries_en = split_long_message(summary_en)

    for part in summaries_cn:
        await client.send_message(-1001826795915, part)
    for part in summaries_cn:
        await client.send_message(-923030708, part)
    # for part in summaries_en:
    #     await client.send_message(-923030708, part)


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
