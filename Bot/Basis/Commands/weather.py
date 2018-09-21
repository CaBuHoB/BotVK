# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_weather_menu_buttons
from Bot.Basis import Configs


def weather(values):
    keyboard = get_weather_menu_buttons(values) if values is not None else None
    return Configs.weatherForecast, None, keyboard


command = command_system.Command()

command.keys = ['погода']
command.description = 'Возвращается прогноз погоды в СПб'
command.process = weather
