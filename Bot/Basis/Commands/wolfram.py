# -*- coding: utf-8 -*-
from Bot.Basis import command_system

import wolframalpha


def wolfram(values):
    task = values.message[values.message.find(' '):]
    client = wolframalpha.Client('V38TWQ-QTKVA595UJ')
    res = client.query(task)
    answer = ''
    for pod in res.pods:
        # if pod.title in ['Result', 'Solutions', 'Expanded form', 'Solution', 'Results']:
        if pod.text is not None:
            answer += '\n' + pod.title + ':\n' + '\n'.join(pod.texts)
    if answer == '':
        answer = 'Что то у меня нет ответа. Я не умею пересылать на столько сложные ответы с сайта:('
    return answer, None, None


command = command_system.Command()

command.keys = ['wolfram', 'вольфрам', 'волфрам']
command.description = 'Обработка заданий с помощью wolfram'
command.process = wolfram
