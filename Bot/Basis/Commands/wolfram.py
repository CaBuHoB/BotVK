# -*- coding: utf-8 -*-
from Bot.Basis import command_system

import wolframalpha


def wolfram(vkApi, message=None, item=None):
    task = message[message.find(' '):]
    client = wolframalpha.Client('V38TWQ-QTKVA595UJ')
    res = client.query(task)
    for pod in res.pods:
        if pod.title in ['Result', 'Solutions', 'Expanded form']:
            res = 'Ответ: ' + '; '.join(pod.texts)
            break
        else:
            res = 'Что то у меня нет ответа. Я не умею такое решать:('
    return res, None, None


hello_command = command_system.Command()

hello_command.keys = ['wolfram', 'вольфрам', 'волфрам']
hello_command.description = 'Просто учусь создавать кнопки. Это полная жесть'
hello_command.process = wolfram
