
---

# Telegram Group Message Recorder

Telegram Group Message Recorder is a bot designed to monitor and record messages from a specific Telegram group. It offers the following features:

- Record every message from a specific Telegram group locally.
- Automatically generate a daily summary of the group's messages.
- Send the daily summary to another group when called upon.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Navigate to the project directory:
```bash
cd TG-recorder
```

3. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Configuration

Before using the bot, certain configurations are required:

1. Rename `config_sample.py` to `config.py`.

2. Fill in the required details in `config.py`, which include:
   - `API_ID` and `API_HASH`: Obtain these from [Telegram's developer portal](https://my.telegram.org).
   - `SESSION_STRING`: This string is required for the bot to authenticate and access Telegram. 
   - `PROXY`: If you're in a region where Telegram is blocked, specify your proxy settings here.

## Usage

1. Start the bot:
```bash
python main.py
```

2. The bot will now monitor the specific group you've set it up for and will record all messages.

3. Every day at 8:00 PM, the bot will automatically send a summary of that day's messages to the designated group.

## Troubleshooting

If you encounter any issues:

1. Ensure you have the correct `API_ID`, `API_HASH`, and `SESSION_STRING`.
2. Ensure your proxy settings are correct if you're using one.
3. Check the error logs for more specific issues and consider [raising an issue](<github-issue-page>) on GitHub.

## Contributing

Feel free to fork this project and submit pull requests. All contributions are welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---