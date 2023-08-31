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
print(summary)