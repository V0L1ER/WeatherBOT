import requests
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_forecast(city: str) -> list:
    forecast_url = (
        f"http://api.openweathermap.org/data/2.5/forecast?"
        f"q={city}&units=metric&appid={WEATHER_API_KEY}"
    )
    response = requests.get(forecast_url)
    data = response.json()
    print("Forecast API response:", data) 
    if "list" in data:
        return data["list"]
    else:
        raise Exception(f"Ошибка получения прогноза погоды. Ответ API: {data}")

def aggregate_daily_forecast(forecasts: list) -> list:
    daily = {}
    for forecast in forecasts:
        dt_txt = forecast.get("dt_txt") 
        if not dt_txt:
            continue
        date_str, time_str = dt_txt.split(" ")
        if date_str not in daily:
            daily[date_str] = forecast
        if time_str == "12:00:00":
            daily[date_str] = forecast
    daily_forecasts = [daily[date] for date in sorted(daily.keys())]
    return daily_forecasts
