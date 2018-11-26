import os
from datetime import datetime

import vk

from Bot.Basis.Functions.getSchedule import getTimetableDict
from Bot.Basis.Functions.getWeatherForecast import getWeather
from Bot.Basis.Threads.QueueThread import QueueThread
from Bot.Basis.Threads.TimetableNotifications import TimetableNotifications
from Bot.Basis.Threads.WeatherThread import WeatherThread

token = os.environ['TOKEN']
confirmation_token = os.environ['CONFIRMATION_TOKEN']

weatherForecast = getWeather()
path = os.path.split(os.path.abspath(__file__))[0]

timetableDict = getTimetableDict()
isUpper = True if (datetime.now().isocalendar()[1] % 2 == 0) else False

session = vk.Session(token)
api = vk.API(session, v=5.85)

api.messages.send(user_id=38081883, message='Бот обновился (:')
api.messages.send(user_id=88195126, message='Бот обновился :)')

notifications_thread = TimetableNotifications(api, timetableDict)
notifications_thread.start()

queue_thread = QueueThread(api)
queue_thread.start()

weather_thread = WeatherThread(api)
weather_thread.start()
