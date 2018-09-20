# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_default_buttons
from Bot.Basis.Functions.MessageReplay import send_msg


# TODO: Не обрабатывает файл, только текст
def infoSendMessage(values):
    from_id = values.item['from_id']
    groups = values.messageFromAdmin[from_id]['groups']
    message_for_groups = values.messageFromAdmin[from_id]['message']

    attachments = []
    for att in message_for_groups['attachments']:
        type = att['type']
        attachments.append(type + '-' + str(att[type]['owner_id']) + '_' + str(att[type]['id']))

    for user in values.users:
        if str(values.users[user]['group']) in groups:
            send_msg(values.vkApi, user, message_for_groups['text'],
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
