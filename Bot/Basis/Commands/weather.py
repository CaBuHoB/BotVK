# -*- coding: utf-8 -*-
from Bot.Basis import command_system

from weather import Weather, Unit


def weather(values):
    weather = Weather(unit=Unit.CELSIUS)
    location = weather.lookup_by_location('petersburg')
    condition = location.condition
    message = condition.date + '\n' + condition.text + '\nTemperature: ' + condition.temp
    return message, None, None


command = command_system.Command()

command.keys = ['погода']
command.description = 'Возвращается прогноз погоды в СПб'
command.process = weather
