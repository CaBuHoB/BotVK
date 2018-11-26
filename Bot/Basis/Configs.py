import os
from datetime import datetime

import vk

from Bot.Basis.Functions.getSchedule import getTimetableDict
from Bot.Basis.Functions.getWeatherForecast import getWeather

token = os.environ['TOKEN']
confirmation_token = os.environ['CONFIRMATION_TOKEN']

weatherForecast = getWeather()
path = os.path.split(os.path.abspath(__file__))[0]

timetableDict = {} #getTimetableDict()
isUpper = True if (datetime.now().isocalendar()[1] % 2 == 0) else False

session = vk.Session(token)
api = vk.API(session, v=5.85)
