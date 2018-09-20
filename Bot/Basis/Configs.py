import json
import os

import vk

from Bot.Basis.Functions.workWithDataBase import getAllUsers
from Bot.Basis.Functions.getSchedule import getDate
from Bot.Basis.Functions.getWeatherForecast import getWeather

# Тестовый бот
token = '07bad0077791b970f09942de845145ae326dc6c6b3d89c03690b1240f4a4a033899cf96e5fa72d6a334bb'
confirmation_token = 'e10e7673'

# Основной бот
# token = '890e1e0743f9afdcf2787f6338c1fd0bc73327a2aa398d8cd38d4e6fdb998b08b43f0a26b905bf25ae47b'
# confirmation_token = 'c9a8cdcb'

users = getAllUsers()
messageFromAdmin = {}
isUpper = getDate()['isUpper']
weatherForecast = getWeather()
path = os.path.abspath(os.path.abspath(__file__))
with open(path + '/Threads/timetable.json', 'r') as f:
    timetableDict = json.load(f)

session = vk.Session(token)
api = vk.API(session, v=5.85)
