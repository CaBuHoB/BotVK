# -*- coding: utf-8 -*-
from Bot.Basis import command_system


def help(vkApi, item=None):
    message = 'Пока я умею только:\n' \
              '1) Отвечать на сообщение \"Hi\"\n' \
              '2) Пересылать твои сообщения\n' \
              '3) Строить таблицу. ' \
              'Если у тебя есть уравнение вида x^2=a (mod p)\n' \
              'Чтобы получить готовую таблицу тебе надо отправить мне сообщение вида \"Крук a p\".' \
              '\nПример: Крук 14 193'
    return message, None, None


hello_command = command_system.Command()

hello_command.keys = ['/help', 'help', 'Помощь', 'помощь']
hello_command.description = 'Помогу тебе'
hello_command.process = help
