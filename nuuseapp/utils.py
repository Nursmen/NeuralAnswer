# rate API
import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup
from num2words import num2words

def rate():
    url = "https://valuta.kg/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    currency_table = soup.find("div", class_="kurs-bar__rates")

    if currency_table:
        rows = currency_table.find_all("div", class_="kurs-bar__item kurs-bar__item--nbkr")
        for row in rows:
            columns = row.find_all("td")
            if len(columns) >= 4:
                currency_usd = columns[0].text.strip()
                currency_eur = columns[1].text.strip()
                currency_rub = columns[2].text.strip()
                currency_kzt = columns[3].text.strip()

                # Convert rate values to words in Russian
                currency_usd_word = num2words(float(currency_usd), lang='ru')
                currency_eur_word = num2words(float(currency_eur), lang='ru')
                currency_rub_word = num2words(float(currency_rub), lang='ru')
                currency_kzt_word = num2words(float(currency_kzt), lang='ru')

                rate = (f"Курс валют на продажу: доллар - {currency_usd_word} сом, евро - {currency_eur_word} сом, "
                        f"рубль - {currency_rub_word} сом, тенге - {currency_kzt_word} сом")
        
                ratenu = (f"Курс валют на продажу: доллар - {currency_usd} сом, евро - {currency_eur} сом, "
                    f"рубль - {currency_rub} сом, тенге - {currency_kzt} сом")
                return rate, ratenu
    
    else:
        return "Валюта не найдена!"


# weather API
import requests
import json

def weather(city, city_translation):
    api_key = 'dbf1c716cecbf43263218e4e0505968c'

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru'
    response = requests.get(url)
    data = json.loads(response.text)

    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    translated_city = city_translation

    temperature_word = num2words(temperature, lang='ru', to='cardinal')
    humidity_word = num2words(humidity, lang='ru', to='cardinal')

    weather = f'Погода в {translated_city}: {weather_description}, Температура: {temperature_word} градусов по цельсию, Влажность: {humidity_word} процента'.replace('запятая', '')
    weathernu = f'Погода в {translated_city}: {weather_description}, Температура: {temperature} градусов по цельсию, Влажность: {humidity} процента'.replace('запятая', '')

    return weather, weathernu

import requests
from bs4 import BeautifulSoup
from num2words import num2words

def rate_en():
    url = "https://valuta.kg/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    currency_table = soup.find("div", class_="kurs-bar__rates")

    if currency_table:
        rows = currency_table.find_all("div", class_="kurs-bar__item kurs-bar__item--nbkr")
        for row in rows:
            columns = row.find_all("td")
            if len(columns) >= 4:
                currency_usd = columns[0].text.strip()
                currency_eur = columns[1].text.strip()
                currency_rub = columns[2].text.strip()
                currency_kzt = columns[3].text.strip()

                currency_usd_word = num2words(float(currency_usd), lang='en')
                currency_eur_word = num2words(float(currency_eur), lang='en')
                currency_rub_word = num2words(float(currency_rub), lang='en')
                currency_kzt_word = num2words(float(currency_kzt), lang='en')

                rate = (f"The exchange rate for dollar is {currency_usd_word}  som, "
                        f"for euro is {currency_eur_word} som, "
                        f"for ruble is {currency_rub_word} som, "
                        f"and for tenge is {currency_kzt_word} som")
                
                ratenu = (f"The exchange rate for dollar is {currency_usd}  som, "
                        f"for euro is {currency_eur} som, "
                        f"for ruble is {currency_rub} som, "
                        f"and for tenge is {currency_kzt} som")
                return rate, ratenu
            
    else:
        return "Currency not found!"



import requests
import json
from num2words import num2words

def weather_en(city):
    api_key = 'dbf1c716cecbf43263218e4e0505968c'

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en'
    response = requests.get(url)

    if response.status_code == 404:
        return "City does not exist."

    data = json.loads(response.text)

    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']

    # Convert temperature and humidity to words
    temperature_word = num2words(int(temperature), lang='en')
    humidity_word = num2words((humidity), lang='en')

    weather = f'Weather in {city}: Temperature: {temperature_word} degrees Celsius, Humidity: {humidity_word} percent'
    weathernu = f'Weather in {city}: Temperature: {temperature} degrees Celsius, Humidity: {humidity} percent'

    return weather, weathernu



# time API
import datetime
from num2words import num2words

def current_time_ru():
    days = {
        1: "первое", 2: "второе", 3: "третье", 4: "четвертое", 5: "пятое",
        6: "шестое", 7: "седьмое", 8: "восьмое", 9: "девятое", 10: "десятое",
        11: "одиннадцатое", 12: "двенадцатое", 13: "тринадцатое", 14: "четырнадцатое", 15: "пятнадцатое",
        16: "шестнадцатое", 17: "семнадцатое", 18: "восемнадцатое", 19: "девятнадцатое", 20: "двадцатое",
        21: "двадцать первое", 22: "двадцать второе", 23: "двадцать третье", 24: "двадцать четвертое", 25: "двадцать пятое",
        26: "двадцать шестое", 27: "двадцать седьмое", 28: "двадцать восьмое", 29: "двадцать девятое", 30: "тридцатое",
        31: "тридцать первое"
    }
    
    months = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
        7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }
    
    now = datetime.datetime.now()
    
    day = now.day
    month = now.month
    hour = now.hour
    minute = now.minute

    day_word = days[day]
    month_word = months[month]
    hour_word = num2words(hour, lang='ru', to='cardinal')
    minute_word = num2words(minute, lang='ru', to='cardinal')
    
    result = f"Сегодня в Бишкеке {day_word} {month_word}, текущее время {hour_word} {minute_word}."
    resultnu = f"Сегодня в Бишкеке {day} {month}, текущее время {hour} {minute}."
    
    return result, resultnu


def current_time_en():
    current_time = datetime.now()
    day_ordinal = num2words(current_time.day, ordinal=True)
    month_name = current_time.strftime("%B")
    hour_word = num2words(current_time.hour if current_time.hour <= 12 else current_time.hour - 12)
    minute_word = num2words(current_time.minute)

    time_period = "am" if current_time.hour < 12 else "pm"

    display = "Today in Bishkek it is {0} of {1}, and the current time is {2} {3} {4}.".format(
        day_ordinal,
        month_name,
        hour_word,
        minute_word,
        time_period
    )

    displaynu = "Today in Bishkek it is {0} of {1}, and the current time is {2} {3} {4}.".format(
        day_ordinal,
        month_name,
        current_time.hour if current_time.hour <= 12 else current_time.hour - 12,
        current_time.minute,
        time_period
    )
    return display, displaynu
