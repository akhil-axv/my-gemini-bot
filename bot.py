import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from google import genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
missing = [
    name
    for name, value in (
        ("TELEGRAM_TOKEN", TELEGRAM_TOKEN),
        ("GEMINI_API_KEY", GEMINI_API_KEY),
    )
    if not value
]
if missing:
    raise SystemExit("Missing environment variable(s): " + ", ".join(missing))

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
ai_client = genai.Client(api_key=GEMINI_API_KEY)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    full_name = html.quote(message.from_user.full_name)
    welcome_text = (
        f"Sálem, <b>{full_name}</b>!\n\n"
        "Men Gemini AI menen isleytuǵın aqıllı botpan. "
        "Maǵan qálegen sorawıńızdı jazıń."
    )
    await message.answer(welcome_text, parse_mode="HTML")


@dp.message(F.text)
async def ai_chat_handler(message: Message) -> None:
    if not message.text:
        return

    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        response = await ai_client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text,
        )
        await message.answer(
            response.text or "AI bos juwap qaytardı. Qayta urınıp kóriń."
        )
    except Exception:
        logger.exception("Gemini request failed")
        await message.answer(
            "Keshiriń, AI juwap beriwde qátelik júz berdi. "
            "Azmazdan soń qayta urınıp kóriń."
        )


async def main() -> None:
    logger.info("Gemini Telegram bot is starting")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
