# -*- coding: utf-8 -*-
from Bot.Basis import command_system


def start(vkApi, item=None):
    message = 'Узнай, что я умею, вызвав help'
    return message, None, None


hello_command = command_system.Command()

hello_command.keys = ['start', 'начало']
hello_command.description = 'Тут надо будет поаботать с регестрацией пользователей'
hello_command.process = start
