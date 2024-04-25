"""
openweathermap:
https://openweathermap.org/current#multi
"""
import requests
from pprint import pprint


def get_weather(city):
    api_key = "8680c2f66daac83d15eba65a61e9ceaf"
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ua&appid={api_key}"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        pprint(data)


        # weather_description = data["weather"][0]["description"]
        # temperature = data["main"]["temp"]
        # feels_like = data["main"]["feels_like"]
        # humidity = data["main"]["humidity"]
        # wind_speed = data["wind"]["speed"]

        # print(f"Погода в городе {city}:")
        # print(f"Описание: {weather_description}")
        # print(f"Температура: {temperature}°C")
        # print(f"Ощущается как: {feels_like}°C")
        # print(f"Влажность: {humidity}%")
        # print(f"Скорость ветра: {wind_speed} м/с")
    else:
        print("Ошибка при получении данных о погоде.")


if __name__ == "__main__":
    # city = input("Введите название города: ")
    get_weather("Kharkiv")
