# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons


def hello(values):
    message = 'Привет, друг!\nЯ новый чат-бот.'
    return message, None, getDefaultScreenButtons()


command = command_system.Command()

command.keys = ['привет', 'hello', 'Hi', 'здравствуй', 'здравствуйте']
command.description = 'Приветствие пользователя'
command.process = hello
