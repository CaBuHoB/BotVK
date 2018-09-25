# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_default_buttons
from Bot.Basis import Configs


def weather(values):
    return Configs.weatherForecast, None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['погода']
command.description = 'Возвращается прогноз погоды в СПб'
command.process = weather
