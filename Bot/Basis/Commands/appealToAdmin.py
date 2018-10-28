# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_default_buttons
from Bot.Basis.Functions.MessageReplay import send_msg


def appealToAdmin(values):
    user_id = values.item['from_id']
    name = values.users[user_id]['name'] + ' ' + values.users[user_id]['surname']

    msg_words = values.item['text'].split()[1:]
    msg = 'Сообщение для админа: \n\n' + \
          ' '.join(msg_words) + '\n\n' + name

    send_msg(values.vkApi, 38081883, msg, attachment=None, keyboard=None)

    return 'Сообщение отправлено администратору )', None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['admin', 'админ']
command.description = 'Обращение к админу'
command.process = appealToAdmin
