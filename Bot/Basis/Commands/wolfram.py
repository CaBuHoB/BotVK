# -*- coding: utf-8 -*-
from Bot.Basis import command_system

import wolframalpha


def wolfram(values):
    task = values.message[values.message.find(' '):]
    client = wolframalpha.Client('V38TWQ-QTKVA595UJ')
    res = client.query(task)
    for pod in res.pods:
        if pod.title in ['Result', 'Solutions', 'Expanded form', 'Solution']:
            res = 'Ответ: ' + '; '.join(pod.texts)
            break
        else:
            res = 'Что то у меня нет ответа. Я не умею пересылать на столько сложные ответы с сайта:('
    return res, None, None


command = command_system.Command()

command.keys = ['wolfram', 'вольфрам', 'волфрам']
command.description = 'Просто учусь создавать кнопки. Это полная жесть'
command.process = wolfram
