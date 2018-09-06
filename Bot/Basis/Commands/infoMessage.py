# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Keyboards.getButtons import get_groups_for_message_buttons


def infoMessage(values):
    message = 'Выбери, для каких групп делать рассылку'
    return message, None, get_groups_for_message_buttons()


command = command_system.Command()

command.keys = ['infoMessage']
command.description = 'Разослать сообщения группам, выбор групп'
command.process = infoMessage
