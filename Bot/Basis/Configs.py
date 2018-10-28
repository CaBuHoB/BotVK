import os
from datetime import datetime

import vk

from Bot.Basis.Functions.getSchedule import getTimetableDict
from Bot.Basis.Functions.getWeatherForecast import getWeather
from Bot.Basis.Threads import TimetableNotifications, QueueThread, WeatherThread

# Тестовый бот
token = '07bad0077791b970f09942de845145ae326dc6c6b3d89c03690b1240f4a4a033899cf96e5fa72d6a334bb'
confirmation_token = 'e10e7673'

# Основной бот
# token = '890e1e0743f9afdcf2787f6338c1fd0bc73327a2aa398d8cd38d4e6fdb998b08b43f0a26b905bf25ae47b'
# confirmation_token = 'c9a8cdcb'

weatherForecast = getWeather()
path = os.path.split(os.path.abspath(__file__))[0]

timetableDict = getTimetableDict()
isUpper = True if (datetime.now().isocalendar()[1] % 2 == 0) else False

session = vk.Session(token)
api = vk.API(session, v=5.85)

api.messages.send(user_id=38081883, message='Бот обновился (:')
api.messages.send(user_id=88195126, message='Бот обновился :)')

notifications_thread = TimetableNotifications.TimetableNotifications(api, timetableDict)
notifications_thread.start()

queue_thread = QueueThread.QueueThread(api)
queue_thread.start()

weather_thread = WeatherThread.WeatherThread(api)
weather_thread.start()
