import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("\U0001F31AПривіт!\U0001F31D\n Напиши мені назву міста і я розповім про погоду в твоєму регіоні!")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Сонячно \U0001F324",
        "Clouds": "Хмарно \U0001F325",
        "Rain": "Дощ \U0001F327",
        "Drizzle": "Дощ \U0001F327",
        "Mist": "Туман \U0001F32B",
        "Thunderstorm": "Гроза \U0001F329",
        "Snow": "Сніг \U0001F328"
    }
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "\U0001F914Подивись у вікно, не розумію що там за погода!\U0001F9D0"

        maxtemp = data["main"]["temp_max"]
        temp = data["main"]["temp"]
        mintemp = data["main"]["temp_min"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lenght_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"****{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}****\n"
              f"\U0001F3D9Погода в місті: {city}\n"f"\U0001F525Максимальна температура: {maxtemp}C°\n"
              f"\U0001F321Сeредня температура: {temp}C°\n{wd}\n"
              f"\U00002744Мінімальна температура: {mintemp}C°\n"
              f"\U0001F4A7Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\n\U0001F32CВітер: {wind} м/год\n"
              f"\U0001F304Світанок: {sunrise_timestamp}\n"
              f"\U0001F307Захід сонця: {sunset_timestamp}\n"
              f"\U0001F3D9Тривалість дня: {lenght_of_the_day}\U0001F306\n"
              f"****Чудового дня!****")

    except:
        await message.reply("\U00002620 Перевірте назву вашого міста \U00002620")

if __name__ == '__main__':
    executor.start_polling(dp)
