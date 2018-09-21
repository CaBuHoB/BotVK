# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_default_buttons
from Bot.Basis.Functions.MessageReplay import send_msg


# TODO: Не обрабатывает докуметы, только текст и изображения
def infoSendMessage(values):
    from_id = values.item['from_id']
    groups = values.messageFromAdmin[from_id]['groups']
    message_for_groups = values.messageFromAdmin[from_id]['message']

    attachments = []
    for att in message_for_groups['attachments']:
        typeFile = att['type']
        attachments.append(typeFile + str(att[typeFile]['owner_id']) + '_' +
                           str(att[typeFile]['id']) + '_' + att[typeFile]['access_key'])

    mes = 'Это тебе:)' if message_for_groups['text'] == '' else message_for_groups['text']

    for user in values.users:
        if str(values.users[user]['group']) in groups:
            send_msg(values.vkApi, user, mes,
                     attachment=attachments, keyboard=None)

    values.messageFromAdmin.pop(from_id)
    message = 'Сообщения разосланы группам: '
    for group in groups:
        message += (' ' + str(group))
    return message, None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['infoSendMessage']
command.description = 'Отправка рассылки информации'
command.process = infoSendMessage
