# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getGroupsForMessageButtons


def infoMessage(values):
    message = 'Для каких групп делать рассылку?'
    return message, None, getGroupsForMessageButtons()


command = command_system.Command()

command.keys = ['infoMessage']
command.description = 'Разослать сообщения группам, выбор групп'
command.process = infoMessage