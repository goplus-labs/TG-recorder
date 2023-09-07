import openai
from config import OPENAI_API_KEY
from message_handler import get_today_messages
import json


def remove_first_last_two_lines(s):
    lines = s.splitlines()
    return '\n'.join(lines[0:-1])


all_messages = get_today_messages()
messages_str = json.dumps(all_messages, indent=2)
messages_text = '\n'.join([msg['text'] for msg in all_messages])
openai.api_key = OPENAI_API_KEY
response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "assistant", "content": f"你是一个中文的群聊总结的助手，你可以为一个telegram的群聊记录，提取并总结每个时间段大家在重点讨论的话题内容。\
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
            以下是群聊内容:"},
            {"role": "user", "content": f"{messages_str}"}
        ]
    )

summary = response.choices[0].message.content.strip()
summary = remove_first_last_two_lines(summary)
print(summary)