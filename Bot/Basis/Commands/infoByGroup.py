# -*- coding: utf-8 -*-
import ast

from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_message_cancel_button
from Bot.Basis.Functions.workWithDataBase import getDictWithMessageFromAdmin, setDictWithMessageFromAdmin


def infoByGroup(values):
    groups = values.item['text'].split()
    dictWithMessageFromAdmin = getDictWithMessageFromAdmin(values.item['from_id'])
    messageFromAdmin = {}
    if dictWithMessageFromAdmin is not None:
        messageFromAdmin = ast.literal_eval(dictWithMessageFromAdmin)
    messageFromAdmin[values.item['from_id']] = {'message': None, 'groups': groups}
    setDictWithMessageFromAdmin(values.item['from_id'], str(messageFromAdmin))
    message = 'Жду сообщения для групп: ' + ' '.join(groups)

    return message, None, get_message_cancel_button()


command = command_system.Command()

command.keys = ['infoByGroup']
command.description = 'Ожидание сообщения для рассылки'
command.process = infoByGroup
