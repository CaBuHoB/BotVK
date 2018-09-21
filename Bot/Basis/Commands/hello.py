# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_default_buttons


def hello(values):
    message = 'Привет!\nЯ чат-бот 52 кафедры СПбГУАП. Чтобы узнать, что я могу, ' \
              'нажми на зелёную кнопку со знаком вопроса. Буду рад тебе помочь!'
    return message, None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['привет', 'hello', 'hi', 'здравствуй', 'здравствуйте']
command.description = 'Приветствие пользователя'
command.process = hello
