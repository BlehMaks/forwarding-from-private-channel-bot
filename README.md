# Telegram Channel Forwarding Bot

## Overview
This is an asynchronous Telegram bot that automatically forwards messages from specified private channels to a target channel. The bot is designed to be run with Python, leveraging the `aiogram` and `pyrogram` libraries for bot and user interactions, respectively. The bot uses encrypted JSON files for storing sensitive configuration data securely.

## Features
- **Automatic Message Forwarding**: Forwards messages (including text, images, etc.) from multiple private channels to a designated target channel.
- **Secure Configuration**: Configuration files are encrypted using the `cryptography` library.
- **Webhook Support**: Utilizes webhooks for efficient communication.
- **User Management**: Supports a list of allowed users, with the ability to dynamically register new users.

## Prerequisites
- **Python 3.7+**: Ensure Python is installed and accessible in your environment.
- **ngrok**: Install ngrok if you plan to test the webhook locally.

    ```bash
    brew install ngrok
    ```

- **Git**: Required if you plan to clone the repository and contribute.

## Installation

### Step 1: Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 2: Install Dependencies
Install the required Python libraries:

```bash
pip install aiogram pyrogram cryptography
```

### Step 3: Set Up Configuration Files
The bot uses encrypted JSON files for its configuration.

- **Bot Configuration (`bot_config.json`)**:
    - `BOT_TOKEN`: Your Telegram bot token.
    - `API_ID`: Your Telegram API ID.
    - `API_HASH`: Your Telegram API hash.
    - `WEBHOOK_URL`: URL for your webhook.
    - `WEBAPP_HOST`: Host for your web app (usually `0.0.0.0`).
    - `WEBAPP_PORT`: Port for your web app (e.g., 8443).
    - `ALLOWED_USER_IDS`: List of user IDs allowed to interact with the bot.

- **User Configuration (`user_config.json`)**:
    - `PHONE_NUMBER`: Phone number for logging into the Telegram account.
    - `PASSWORD`: Password for the Telegram account.
    - `TARGET_CHANNEL_ID`: ID of the target channel where messages will be forwarded.
    - `SOURCE_CHANNEL_IDS`: List of channel IDs to monitor and forward messages from.

### Step 4: Encrypt Configuration Files
After creating your JSON configuration files, encrypt them:

```python
from config import BotConfig, UserConfig, save_bot_config, save_user_config


# Encrypt the bot configuration
bot_config = BotConfig(
    BOT_TOKEN="your_bot_token",
    API_ID=123456,
    API_HASH="your_api_hash",
    WEBHOOK_URL="https://your-domain.com",
    WEBAPP_HOST="0.0.0.0",
    WEBAPP_PORT=8443,
    ALLOWED_USER_IDS=[123456789]
)
save_bot_config(bot_config)

# Encrypt the user configuration
user_config = UserConfig(
    PHONE_NUMBER="+1234567890",
    PASSWORD="your_password",
    TARGET_CHANNEL_ID=-1001234567890,
    SOURCE_CHANNEL_IDS=[-1009876543210]
)
save_user_config(user_config)
```

### Step 5: Run the Bot
Run the bot using the following command:

```bash
python main.py
```

## Usage

### Commands
- `/start`: Initializes the bot and registers the user if not already in the allowed list.
- `/help`: Provides a brief description of the bot’s functionality.

### Webhook Configuration
For testing locally, use ngrok to expose your local server to the internet:

```bash
ngrok http 8443
```

Use the ngrok URL for the `WEBHOOK_URL` in your `bot_config.json` file.

## Logging
All bot actions, errors, and events are logged in the `bot.log` file for easy debugging and monitoring.

## Security Considerations
- **Encryption**: All configuration files are encrypted for security.
- **Access Control**: Only registered and allowed users can interact with the bot.

## Versioning
This bot follows a versioning system. The current version is 5.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License.