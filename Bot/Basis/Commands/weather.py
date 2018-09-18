# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

from Bot.Basis import command_system
from Bot.Basis.Keyboards.getButtons import get_default_buttons


def weather(values):
    url = 'https://weather.com/ru-RU/weather/today/l/RSXX0091:1:RS'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="lxml")

    # погода текущая
    weatherNow = soup.find('div', attrs={'class': ['today_nowcard-main'], 'style': ''})
    caption = weatherNow.find('header')
    city = weatherNow.find('span').text
    time = caption.find('p').text
    weather = city + ' ' + time + '\n'
    temp = weatherNow.find('div', attrs={'class': ['today_nowcard-temp']}).text
    phrase = weatherNow.find('div', attrs={'class': ['today_nowcard-phrase']}).text
    weather += 'Сейчас: ' + temp + ' ' + phrase + '\n'
    feels = weatherNow.find('div', attrs={'class': ['today_nowcard-feels']}).text
    weather += feels + '\n'
    hilo = weatherNow.find('div', attrs={'class': ['today_nowcard-hilo']}).text[:13]
    hilo = ''.join(hilo.split(' '))
    sidecar = soup.find('div', attrs={'class': ['today_nowcard-sidecar']})
    humidity = sidecar.find_all('tr')[1]
    humidity = humidity.find('th').text + ': ' + humidity.find('td').text
    weather += humidity + '\n'
    weather += 'Сегодня: ' + hilo
    return weather, None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['погода']
command.description = 'Возвращается прогноз погоды в СПб'
command.process = weather
