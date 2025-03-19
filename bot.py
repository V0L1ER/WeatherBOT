import os
import asyncio
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from weather import get_forecast, aggregate_daily_forecast

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот прогноза погоды. Отправь мне название города, и я пришлю тебе прогноз погоды на несколько дней вперед."
    )

@dp.message()
async def handle_city(message: Message):
    city = message.text.strip()
    await message.answer(f"Получаю прогноз погоды для города: {city}...")
    try:
        forecasts = get_forecast(city)
        daily_forecasts = aggregate_daily_forecast(forecasts)
        forecast_message = f"Прогноз погоды для <b>{city}</b>:\n\n"
        for forecast in daily_forecasts:
            date = datetime.datetime.fromtimestamp(forecast["dt"]).strftime("%d.%m.%Y")
            temp_day = forecast["main"]["temp"]
            description = forecast["weather"][0]["description"].capitalize()
            forecast_message += f"{date}: {description}, температура: {temp_day}°C\n"
        await message.answer(forecast_message, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Ошибка при получении прогноза: {e}")

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
