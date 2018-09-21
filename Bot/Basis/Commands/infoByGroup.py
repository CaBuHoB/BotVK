# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_message_cancel_button


def infoByGroup(values):
    groups = values.item['text'].split(' ')
    values.messageFromAdmin[values.item['from_id']] = {'message': None, 'groups': groups}
    message = 'Жду сообщения для групп:'
    for group in groups:
        message += (' ' + str(group))
    message += '\n\nПодпишись в конце сообщения, если хочешь, чтоб было понятно, от кого оно :)'
    return message, None, get_message_cancel_button()


command = command_system.Command()

command.keys = ['infoByGroup']
command.description = 'Ожидание сообщения для рассылки'
command.process = infoByGroup
