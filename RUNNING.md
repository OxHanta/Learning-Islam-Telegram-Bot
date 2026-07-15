# Running the Islamic Learning Bot

This guide explains how to configure, run, and host the Islamic Learning Bot on any standard platform (such as a local machine, Virtual Private Server (VPS), Docker, Heroku, or other cloud providers).

## Prerequisites
- **Python 3.10+**
- **SQLite3** (usually pre-installed with Python)
- A Telegram bot token (from [@BotFather](https://t.me/BotFather))
- An OpenAI API Key (optional, for the AI conversation feature)

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Learning-Islam-Telegram-Bot
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The bot is configured using environment variables. Set the following variables before running:

- `TELEGRAM_BOT_TOKEN`: **Required.** Your Telegram bot API token.
- `OPENAI_API_KEY`: **Optional.** Your OpenAI API key for natural AI learning conversations.
- `OPENAI_BASE_URL`: **Optional.** Set if you are using an OpenAI-compatible proxy or alternative endpoint.
- `OPENAI_MODEL`: **Optional.** Defaults to `gpt-5` (or any model of your choice, like `gpt-4o`).

### Setting Environment Variables

On Linux/macOS:
```bash
export TELEGRAM_BOT_TOKEN="your-telegram-token-here"
export OPENAI_API_KEY="your-openai-api-key-here"
```

On Windows (Command Prompt):
```cmd
set TELEGRAM_BOT_TOKEN=your-telegram-token-here
set OPENAI_API_KEY=your-openai-api-key-here
```

On Windows (PowerShell):
```powershell
$env:TELEGRAM_BOT_TOKEN="your-telegram-token-here"
$env:OPENAI_API_KEY="your-openai-api-key-here"
```

## Running the Bot

Start the bot by executing the python package runner:

```bash
python -m bot.main
```

Once started, the database (`islamic_bot.db`) will be automatically created and populated with curated initial data if it doesn't already exist.
