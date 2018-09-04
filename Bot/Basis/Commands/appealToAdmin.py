# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons
from Bot.Basis.MessageReplay import send_msg


def appealToAdmin(values):
    admin_id = 38081883
    id = values.item['from_id']
    name = values.users[id]['name'] + ' ' + values.users[id]['surname']
    msg_words = values.item['text'].split(' ')[1:]
    msg = 'Сообщение для админа: \n\n' + \
          ' '.join(msg_words) + '\n\n' + name
    send_msg(values.vkApi.get_api(), admin_id, msg, attachment=None, keyboard=None)
    message = 'Сообщение отправлено администратору )'
    return message, None, getDefaultScreenButtons(values)


command = command_system.Command()

command.keys = ['admin']
command.description = 'Обращение к админу'
command.process = appealToAdmin
