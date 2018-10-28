import os
import threading
from datetime import datetime

import vk

from Bot.Basis.Functions.getSchedule import getTimetableDict
from Bot.Basis.Functions.getWeatherForecast import getWeather
from Bot.Basis.Threads import TimetableNotifications, QueueThread, WeatherThread

token = os.environ['TOKEN']
confirmation_token = os.environ['CONFIRMATION_TOKEN']

weatherForecast = getWeather()
path = os.path.split(os.path.abspath(__file__))[0]

timetableDict = getTimetableDict()
isUpper = True if (datetime.now().isocalendar()[1] % 2 == 0) else False

session = vk.Session(token)
api = vk.API(session, v=5.85)

with threading.Lock():
    if os.environ['START_THREADS'] == 'true':
        notifications_thread = TimetableNotifications.TimetableNotifications(api, timetableDict)
        notifications_thread.start()

        queue_thread = QueueThread.QueueThread(api)
        queue_thread.start()

        weather_thread = WeatherThread.WeatherThread(api)
        weather_thread.start()

        api.messages.send(user_id=38081883, message='Бот обновился (:')
        api.messages.send(user_id=88195126, message='Бот обновился :)')
        os.environ['test'] = 'false'
