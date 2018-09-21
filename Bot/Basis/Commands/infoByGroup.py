# -*- coding: utf-8 -*-
import ast

from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_message_cancel_button
from Bot.Basis.Functions.workWithDataBase import getDictWithMessageFromAdmin, setDictWithMessageFromAdmin


def infoByGroup(values):
    groups = values.item['text'].split(' ')
    messageFromAdmin = ast.literal_eval(getDictWithMessageFromAdmin(values.item['from_id']))
    messageFromAdmin[values.item['from_id']] = {'message': None, 'groups': groups}
    setDictWithMessageFromAdmin(values.item['from_id'], str(messageFromAdmin))
    message = 'Жду сообщения для групп: ' + ' '.join(groups)
    message += '\n\nПодпишись в конце сообщения, если хочешь, чтоб было понятно, от кого оно :)'
    return message, None, get_message_cancel_button()


command = command_system.Command()

command.keys = ['infoByGroup']
command.description = 'Ожидание сообщения для рассылки'
command.process = infoByGroup
