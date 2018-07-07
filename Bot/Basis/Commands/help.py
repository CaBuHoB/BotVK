# -*- coding: utf-8 -*-
from Bot.Basis import command_system


def help(values):
    message = 'Пока я умею только:\n' \
              '1) Отвечать на сообщение \"Hi\"\n' \
              '2) Пересылать твои сообщения\n' \
              '3) Строить таблицу. ' \
              'Если у тебя есть уравнение вида x^2=a (mod p)\n' \
              'Чтобы получить готовую таблицу тебе надо отправить мне сообщение вида \"Крук a p\".' \
              '\nПример: Крук 14 193'
    return message, None, None


command = command_system.Command()

command.keys = ['/help', 'help', 'Помощь', 'помощь']
command.description = 'Помогу тебе'
command.process = help
