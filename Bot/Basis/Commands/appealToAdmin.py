# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons
from Bot.Basis.MessageReplay import send_msg


def appealToAdmin(values):
    admin_id = 38081883
    msg_words = values.item['text'].split(' ')[1:]
    msg = 'Сообщение от ' + str(values.item['from_id']) + ' (Тут должно быть имя по айди из БД)\n\n' + \
          ' '.join(msg_words)
    send_msg(values.vkApi.get_api(), admin_id, msg, attachment=None, keyboard=None)
    message = 'Сообщение отправлено администратору )'
    return message, None, getDefaultScreenButtons()


command = command_system.Command()

command.keys = ['admin']
command.description = 'Обращение к админу'
command.process = appealToAdmin
