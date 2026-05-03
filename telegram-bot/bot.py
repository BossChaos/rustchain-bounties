#!/usr/bin/env python3
"""
RustChain Telegram Bot - Bounty #2869
Provides wallet balance, miner stats, epoch info, and RTC price via Telegram.
"""

import asyncio
import logging
import os
import time
from datetime import datetime, timezone

import httpx
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
API_BASE = os.getenv("RUSTCHAIN_API", "https://50.28.86.131")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RATE_LIMIT_SECONDS = 5  # per user

if not BOT_TOKEN:
    raise SystemExit(
        "Error: TELEGRAM_BOT_TOKEN environment variable must be set."
    )

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------
_user_last_request: dict[int, float] = {}


def _check_rate_limit(user_id: int) -> bool:
    """Return True if the request is allowed, False if rate-limited."""
    now = time.monotonic()
    last = _user_last_request.get(user_id, 0)
    if now - last < RATE_LIMIT_SECONDS:
        return False
    _user_last_request[user_id] = now
    return True


async def _send_rate_limit_msg(update: Update) -> None:
    await update.message.reply_text(
        f"⏳ Rate limited — please wait {RATE_LIMIT_SECONDS}s between requests."
    )


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------
async def _api_get(path: str, timeout: float = 15) -> dict | list | None:
    """GET from the RustChain API, returning parsed JSON or None on error."""
    url = f"{API_BASE}{path}"
    try:
        async with httpx.AsyncClient(
            verify=False, timeout=timeout
        ) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()
    except httpx.TimeoutException:
        logger.error("Request to %s timed out", url)
        return None
    except httpx.HTTPStatusError as exc:
        logger.error("HTTP error for %s: %s", url, exc)
        return None
    except Exception as exc:
        logger.error("Request to %s failed: %s", url, exc)
        return None


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------
async def cmd_balance(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """/balance <wallet_id> — Query a wallet's RTC balance."""
    if not _check_rate_limit(update.effective_user.id):
        await _send_rate_limit_msg(update)
        return

    args = ctx.args
    if not args:
        await update.message.reply_text(
            "Usage: /balance <wallet_id>\n"
            "Example: /balance RTC6d1f27d28961279f1034d9561c2403697eb55602"
        )
        return

    wallet_id = args[0]
    data = await _api_get(f"/wallet/balance?wallet_id={wallet_id}")

    if data is None:
        await update.message.reply_text(
            f"❌ Failed to fetch balance for <code>{wallet_id}</code>. "
            "Please try again later.",
            parse_mode="HTML",
        )
        return

    balance = data.get("balance", data.get("result", data))
    await update.message.reply_text(
        f"💰 Wallet: <code>{wallet_id}</code>\n"
        f"Balance: <b>{balance}</b> RTC",
        parse_mode="HTML",
    )


async def cmd_miners(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """/miners — Show miner statistics."""
    if not _check_rate_limit(update.effective_user.id):
        await _send_rate_limit_msg(update)
        return

    data = await _api_get("/api/miners")

    if data is None:
        await update.message.reply_text(
            "❌ Failed to fetch miner data. Please try again later."
        )
        return

    # Handle both list and dict responses
    if isinstance(data, list):
        total = len(data)
        active = sum(1 for m in data if m.get("status") == "active")
        msg = f"⛏️ Total miners: <b>{total}</b>\n" f"Active: <b>{active}</b>"
        # Show top 5 by stake/hashrate if available
        miners = sorted(
            data,
            key=lambda m: (
                m.get("stake", m.get("hashrate", m.get("power", 0)))
            ),
            reverse=True,
        )[:5]
        if miners:
            msg += "\n\n<b>Top 5 miners:</b>\n"
            for i, m in enumerate(miners, 1):
                addr = m.get("address", m.get("wallet", "N/A"))[:18] + "..."
                stake = m.get("stake", m.get("hashrate", m.get("power", "N/A")))
                msg += f"{i}. <code>{addr}</code> — {stake}\n"
    elif isinstance(data, dict):
        msg = "⛏️ Miner Stats:\n"
        for k, v in data.items():
            msg += f"• {k}: <b>{v}</b>\n"
    else:
        msg = f"⛏️ {data}"

    await update.message.reply_text(msg, parse_mode="HTML", disable_web_page_preview=True)


async def cmd_epoch(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """/epoch — Show current epoch info."""
    if not _check_rate_limit(update.effective_user.id):
        await _send_rate_limit_msg(update)
        return

    data = await _api_get("/epoch")

    if data is None:
        await update.message.reply_text(
            "❌ Failed to fetch epoch data. Please try again later."
        )
        return

    msg = "🔄 <b>Epoch Info:</b>\n"
    if isinstance(data, dict):
        for k, v in data.items():
            msg += f"• {k}: <b>{v}</b>\n"
    else:
        msg += str(data)

    await update.message.reply_text(msg, parse_mode="HTML")


async def cmd_price(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """/price — Show RTC price (from API or fallback)."""
    if not _check_rate_limit(update.effective_user.id):
        await _send_rate_limit_msg(update)
        return

    # Try API first
    data = await _api_get("/price")

    msg = "📈 <b>RTC Price:</b>\n"
    if data and isinstance(data, dict):
        for k, v in data.items():
            msg += f"• {k}: <b>${v}</b>\n"
    elif data:
        msg += f"Price: <b>${data}</b>\n"
    else:
        # Fallback: try fetching from a public API
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    "https://api.coingecko.com/api/v3/simple/price",
                    params={"ids": "rustchain", "vs_currencies": "usd"},
                )
                if resp.status_code == 200:
                    info = resp.json()
                    price = info.get("rustchain", {}).get("usd", "N/A")
                    msg += f"• USD: <b>${price}</b> (CoinGecko)\n"
                else:
                    msg += "• Price data currently unavailable.\n"
        except Exception:
            msg += "• Price data currently unavailable.\n"

    await update.message.reply_text(msg, parse_mode="HTML")


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """/help — Show available commands."""
    help_text = (
        "🤖 <b>RustChain Telegram Bot</b>\n\n"
        "<b>Commands:</b>\n"
        "• /balance &lt;wallet_id&gt; — Check wallet balance\n"
        "• /miners — View miner statistics\n"
        "• /epoch — Get current epoch info\n"
        "• /price — Check RTC token price\n"
        "• /help — Show this help message\n\n"
        f"⏱️ Rate limit: 1 request per {RATE_LIMIT_SECONDS}s per user\n\n"
        "<b>Examples:</b>\n"
        "<code>/balance RTC6d1f27d28961279f1034d9561c2403697eb55602</code>\n"
        "<code>/miners</code>\n"
        "<code>/epoch</code>\n"
        "<code>/price</code>"
    )
    await update.message.reply_text(help_text, parse_mode="HTML")


async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """/start — Welcome message."""
    await cmd_help(update, ctx)


async def handle_unknown(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle non-command messages."""
    pass  # Ignore non-command messages


async def error_handler(update: object, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Log and handle errors."""
    logger.error("Exception while handling an update:", exc_info=ctx.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ An error occurred. Please try again later."
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    """Start the bot."""
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .connect_timeout(10)
        .read_timeout(10)
        .write_timeout(10)
        .get_updates_connect_timeout(30)
        .build()
    )

    # Register command handlers
    application.add_handler(CommandHandler("start", cmd_start))
    application.add_handler(CommandHandler("help", cmd_help))
    application.add_handler(CommandHandler("balance", cmd_balance))
    application.add_handler(CommandHandler("miners", cmd_miners))
    application.add_handler(CommandHandler("epoch", cmd_epoch))
    application.add_handler(CommandHandler("price", cmd_price))

    # Error handler
    application.add_error_handler(error_handler)

    logger.info("RustChain Bot starting...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
