import os
import time

import vk

from Bot.Basis import Configs
from Bot.Basis.Threads import TimetableNotifications, QueueThread, WeatherThread


def start(timetableDict):
    time.sleep(1)

    session = vk.Session(os.environ['TOKEN'])
    api = vk.API(session, v=5.85)

    notifications_thread = TimetableNotifications.TimetableNotifications(api, timetableDict)
    notifications_thread.name = 'TimetableNotifications'
    notifications_thread.start()

    queue_thread = QueueThread.QueueThread(api)
    queue_thread.start()

    weather_thread = WeatherThread.WeatherThread(api)
    weather_thread.start()

    api.messages.send(user_id=38081883, message='Бот обновился (:')
    api.messages.send(user_id=88195126, message='Бот обновился :)')

    time.sleep(1)


start(Configs.timetableDict)
