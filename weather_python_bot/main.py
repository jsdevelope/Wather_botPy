import requests
import telebot
from config import tg_bot_token
import datetime
from pprint import pprint
from config import open_weather_token


def get_weather(city, open_weather_token):

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
         f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data)

        city = data["name"]
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Подивись у вікно, не розумію що там за погода!"

        maxtemp = data["main"]["temp_max"]
        temp = data["main"]["temp"]
        mintemp = data["main"]["temp_min"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lenght_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        print(f"****{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}****\n"
              f"Погода в місті: {city}\n"f"Максимальна температура: {maxtemp}C°\n"
              f"Сeредня температура: {temp}C°{wd}\n"
              f"Мінімальна температура: {mintemp}C°\n"
              f"Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\nВітер: {wind} м/год\n"
              f"Світанок: {sunrise_timestamp}\n"
              f"Захід сонця: {sunset_timestamp}\n"
              f"Тривалість дня: {lenght_of_the_day}\n"
              f"****Чудового дня!****")

    except Exception as ex:
        print(ex)
        print("Перевірте назву вашого міста")


def main():
    city = input("Напишіть назву вашого міста: ")
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()



