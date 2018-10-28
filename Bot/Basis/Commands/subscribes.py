# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_sub_buttons


def subscribes(values):
    return 'Меню подписок', None, get_sub_buttons(values)


command = command_system.Command()

command.keys = ['subscribes']
command.description = 'Подписки'
command.process = subscribes
