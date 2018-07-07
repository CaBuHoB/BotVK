# -*- coding: utf-8 -*-
from Bot.Basis import command_system


def hello(values):
    message = 'Привет, друг!\nЯ новый чат-бот.'
    return message, None, None


command = command_system.Command()

command.keys = ['привет', 'hello', 'Hi', 'здравствуй', 'здравствуйте']
command.description = 'Поприветствую тебя'
command.process = hello
