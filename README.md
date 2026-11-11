# My Gemini Bot

An asynchronous Telegram chatbot built with aiogram and Google's Gemini API.

## Features

- Responds to text messages.
- Uses asynchronous Telegram and Gemini clients.
- Reads credentials from environment variables.
- Logs errors for maintainers while keeping user-facing messages simple.

## Requirements

- Python 3.10+
- Telegram bot token
- Gemini API key

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Set `TELEGRAM_TOKEN` and `GEMINI_API_KEY` in `.env`, then run:

```bash
set -a
. ./.env
set +a
python bot.py
```

## Security

Do not commit environment files or paste secrets into source code. Revoke any credentials that were previously committed. Be mindful that user messages are sent to an external AI service for processing.

## Project files

- `bot.py`: bot startup and message handlers
- `requirements.txt`: runtime dependencies
- `.env.example`: configuration template
