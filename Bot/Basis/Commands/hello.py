# -*- coding: utf-8 -*-
from Bot.Basis import command_system


def hello(vkApi, item=None):
    message = 'Привет, друг!\nЯ новый чат-бот.'
    return message, None, None


hello_command = command_system.Command()

hello_command.keys = ['привет', 'hello', 'Hi', 'здравствуй', 'здравствуйте']
hello_command.description = 'Поприветствую тебя'
hello_command.process = hello
