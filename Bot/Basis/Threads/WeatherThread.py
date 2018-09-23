# -*- coding: utf-8 -*-
import datetime as dt
from argparse import Namespace
from threading import Thread

import time

from Bot.Basis.Commands.weather import weather
from Bot.Basis.Functions.getWeatherForecast import getWeather
from Bot.Basis.Functions.workWithDataBase import getSubscribedUsersWeather, getAllUsers
from Bot.Basis.Functions.getButtons import get_default_buttons


def send_day_weather(vk):
    users = getAllUsers()
    message = 'Доброе утро) Рассылка погоды :)\n\n' + getWeather()
    for user in getSubscribedUsersWeather():
        vk.messages.send(user_id=user, message=message, attachment=None,
                         keyboard=get_default_buttons(Namespace(users=users), users_id=user))


class WeatherThread(Thread):

    def __init__(self, vk):
        Thread.__init__(self)
        self.vk = vk

    def run(self):
        while True:
            now = dt.datetime.now()
            then = dt.datetime(now.timetuple()[0], now.timetuple()[1], now.timetuple()[2], 9, 0)
            difference = (then - now).total_seconds()

            if difference < 0:  # если в этом дне время рассылки прошло
                                  # заснуть до 0:01, начать цикл заново
                now += dt.timedelta(1)
                then = dt.datetime(now.timetuple()[0], now.timetuple()[1], now.timetuple()[2], 0, 1)
                now -= dt.timedelta(1)
                time.sleep((then - now).total_seconds())  # Сон до 00:01
            else:
                if difference >= 0:
                    time.sleep(difference)
                send_day_weather(self.vk)
