# -*- coding: utf-8 -*-
import ast

from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_default_buttons
from Bot.Basis.Functions.MessageReplay import send_msg


# TODO: Не обрабатывает докуметы, только текст и изображения
from Bot.Basis.Functions.workWithDataBase import getDictWithMessageFromAdmin, deleteDictWithMessageFromAdmin


def infoSendMessage(values):
    from_id = values.item['from_id']

    messageFromAdmin = ast.literal_eval(getDictWithMessageFromAdmin(from_id))
    groups = messageFromAdmin[from_id]['groups']
    message_for_groups = messageFromAdmin[from_id]['message']

    attachments = []
    for att in message_for_groups['attachments']:
        typeFile = att['type']
        attachments.append(typeFile + str(att[typeFile]['owner_id']) + '_' +
                           str(att[typeFile]['id']) + '_' + att[typeFile]['access_key'])

    mes = message_for_groups['text']
    if (values.users[from_id]['surname'] != 'Савинов') and (values.users[from_id]['surname'] != 'Борисова'):
        mes += '\n\n(' + values.users[from_id]['name'] + ' ' + values.users[from_id]['surname'] + ')'

    if mes == '':
        mes = 'Рассылка от администратора )'

    for user in values.users:
        if str(values.users[user]['group']) in groups:
            send_msg(values.vkApi, user, mes, attachment=attachments, keyboard=None)

    deleteDictWithMessageFromAdmin(from_id)
    message = 'Сообщения разосланы группам: '
    for group in groups:
        message += (' ' + str(group))
    return message, None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['infoSendMessage']
command.description = 'Отправка рассылки информации'
command.process = infoSendMessage
