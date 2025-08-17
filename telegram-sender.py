import asyncio
from telegram import Bot, Update
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv
import os

load_dotenv()

## Bot-Name: chatbot
## Bot-Username: @call518Bot
TELEGRAM_TOKEN :str = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID :int = os.getenv("TELEGRAM_CHAT_ID")

## Bot-Name: Perplexis
## Bot-Username: @Perplexis_Bot
async def send_message(msg: str) -> None:
    msg = escape_markdown(msg, version=2)
    bot = Bot(token=TELEGRAM_TOKEN)
    async with bot:
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=msg,
            parse_mode=ParseMode.MARKDOWN_V2,
        )

text = """
# [테스트] 안녕하세요.
- test1
- test2
"""

asyncio.run(send_message(text))