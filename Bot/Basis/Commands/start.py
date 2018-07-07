# -*- coding: utf-8 -*-
from Bot.Basis import command_system


def start(values):
    message = 'Узнай, что я умею, вызвав help'
    return message, None, None


command = command_system.Command()

command.keys = ['start', 'начало']
command.description = 'Тут надо будет поаботать с регестрацией пользователей'
command.process = start
