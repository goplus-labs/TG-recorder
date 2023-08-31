import datetime
from message_handler import all_messages


async def send_report(event):
    if "@your_username" in event.text:
        current_date = datetime.datetime.now().date()
        report = f"Report for {current_date}:\n"
        for msg in all_messages:
            if msg['date'].date() == current_date:
                report += f"{msg['user']}: {msg['text']}\n"

        await event.reply(report)

