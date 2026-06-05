import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, html, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from google import genai

# --- QÁWİPSİZ SAZLAWLAR ---
# Railway saytındaǵı variables bóliminen kiltlerdi avtomat oqıydb
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Bot, Dispatcher hám AI Clientti baslaw
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
ai_client = genai.Client(api_key=GEMINI_API_KEY)

logging.basicConfig(level=logging.INFO)

# --- /start buyrıǵı ---
@dp.message(CommandStart())
async def command_start_handler(message: Message):
    welcome_text = (
        f"Sálem, {html.bold(message.from_user.full_name)}!\n\n"
        f"🧠 Men **Gemini AI** menen isleytuǵın aqıllı botıman.\n"
        f"Maǵan qálegen sorawıńızdı jazıń, men sizge juwap beremen! ✨"
    )
    await message.answer(welcome_text, parse_mode="HTML")

# --- AI menen chat bólimi ---
@dp.message(F.text)
async def ai_chat_handler(message: Message):
    # Bot juwap bergenshe "typing..." statusın kórsetip turadı
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    try:
        # Gemini-2.5-flash modeline soraw jiberiw
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
        )
        # AI juwaptı Markdown formatında jiberiw
        await message.answer(response.text, parse_mode="Markdown")
        
    except Exception as e:
        logging.error(f"AI qáteligi: {e}")
        await message.answer("⚠️ Keşiresiz, AI juwap beriwde qátelik júz berdi. Azmazdan soń qayta urınıp kórıń.")

# --- BOTTI ISKE TÚSÍRÍW ---
async def main():
    print("Gemini AI Bot iske tústi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
