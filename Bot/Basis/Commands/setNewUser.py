# -*- coding: utf-8 -*-
from Bot.Basis import command_system


def setNewUser(values):
    # TODO конечно же здесь все надо переделать. Добовлять всю информацию пользователя в БД и в список локальный
    message = 'Поздравляю, ты зарегистрирован!'
    values.users[values.item['user_id']] = ''
    return message, None, None


command = command_system.Command()

command.keys = ['setNewUser']
command.description = 'Здесь добовляем пользователя'
command.process = setNewUser
