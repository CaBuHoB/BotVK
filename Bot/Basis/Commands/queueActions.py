from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import getQueueList
from Bot.Basis.Keyboards.GetButtons import getQueueActionsButtons


def queueActions(values):
    queue = values.item['text']
    if queue == '⟵ в меню этой очереди':
        queue = values.message.split(' ')[1]
    connect = values.connect

    message = 'Название очереди: ' + queue

    list = getQueueList(connect, queue)
    if len(list) < 1:
        message += '\nВ этой очереди ещё никто не записан'
    else:
        message += '\n\nСписок:'
        for name in list:
            message += '\n'
            message += name
    keyboard = getQueueActionsButtons(queue)
    return message, None, keyboard


command = command_system.Command()

command.keys = ['queueActions']
command.description = 'Кнопки для выбора действия в очереди'
command.process = queueActions
