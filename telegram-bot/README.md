# RustChain Telegram Bot

A Telegram bot for interacting with the RustChain network — check wallet balances, view miner statistics, get epoch info, and track the RTC token price.

## Features

- 💰 `/balance <wallet_id>` — Check a wallet's RTC balance
- ⛏️ `/miners` — View miner statistics and top miners
- 🔄 `/epoch` — Get current epoch information
- 📈 `/price` — Check RTC token price
- 🤖 `/help` — Show available commands

## Requirements

- Python 3.10+
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/BossChaos/rustchain-telegram-bot.git
cd rustchain-telegram-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the bot

Set the required environment variable:

```bash
export TELEGRAM_BOT_TOKEN="your-bot-token-here"
```

Optionally, set a custom RustChain API endpoint:

```bash
export RUSTCHAIN_API="https://50.28.86.131"
```

### 4. Run the bot

```bash
python bot.py
```

The bot will start polling for messages and respond to commands.

## Deployment

### Using systemd (Linux)

1. Create a service file:

```bash
sudo nano /etc/systemd/system/rustchain-bot.service
```

2. Add the following content (adjust paths as needed):

```ini
[Unit]
Description=RustChain Telegram Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/rustchain-telegram-bot
Environment=TELEGRAM_BOT_TOKEN=your-bot-token-here
Environment=RUSTCHAIN_API=https://50.28.86.131
ExecStart=/usr/bin/python3 /path/to/rustchain-telegram-bot/bot.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable rustchain-bot
sudo systemctl start rustchain-bot
```

4. Check the status:

```bash
sudo systemctl status rustchain-bot
```

### Using Docker

1. Create a `Dockerfile`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bot.py .
CMD ["python", "bot.py"]
```

2. Build and run:

```bash
docker build -t rustchain-bot .
docker run -d \
  --name rustchain-bot \
  -e TELEGRAM_BOT_TOKEN=your-bot-token-here \
  -e RUSTCHAIN_API=https://50.28.86.131 \
  --restart unless-stopped \
  rustchain-bot
```

### Using pm2

```bash
npm install -g pm2
pm2 start "python bot.py" --name rustchain-bot
pm2 save
pm2 startup
```

## Rate Limiting

The bot enforces a rate limit of **1 request per 5 seconds per user** to prevent API abuse. If a user sends commands too frequently, they will receive a rate limit notification.

## Error Handling

- Network timeouts are caught and reported gracefully
- HTTP errors are logged and user-friendly messages are displayed
- Unexpected errors are logged and a generic error message is shown to users

## License

MIT

## Bounty

This bot was created for RustChain Bounty [#2869](https://github.com/rustchain-bounties/bounties/issues/2869).
