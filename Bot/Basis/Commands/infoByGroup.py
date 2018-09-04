# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getMessageEscapeButton


def infoByGroup(values):
    id = values.item['from_id']
    groups = values.item['text'].split(' ')
    values.messageFromAdmin.setdefault(id, {'message': None, 'groups': groups})
    message = 'Жду сообщения для групп:'
    for group in groups:
        message += (' ' + str(group))
    return message, None, getMessageEscapeButton()


command = command_system.Command()

command.keys = ['infoByGroup']
command.description = 'Ожидание сообщения для рассылки'
command.process = infoByGroup