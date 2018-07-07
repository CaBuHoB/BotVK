# -*- coding: utf-8 -*-
from Bot.Basis import command_system


def setNewUser(values):
    # конечно же здесь все по другому
    message = 'Поздравляю, ты зарегистрирован!'
    values.user_ids.append(values.item['user_id'])
    return message, None, None


command = command_system.Command()

command.keys = ['setNewUser']
command.description = 'Здесь добовляем пользователя'
command.process = setNewUser
