# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getButtonsForRegistration


def registration(values):
    if values.item['user_id'] in values.user_ids:
        return 'Ты уже зарегистрирован, расслабься🙃', None, None
    message = 'Выбери'
    return message, None, getButtonsForRegistration()


command = command_system.Command()

command.keys = ['регистрация']
command.description = 'Тут регистрируем полтзователя'
command.process = registration
