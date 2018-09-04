from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import getQueueList
from Bot.Basis.Keyboards.GetButtons import getQueueActionsButtons


def queueActions(values):
    id = values.item['from_id']
    queue = values.item['text']
    if queue == '⟵ в меню этой очереди':
        queue = values.message.split()[1]

    queue_name = '\"' + queue + '\"'
    connect = values.connect
    list = getQueueList(connect, queue_name)
    message = 'Название очереди: ' + queue
    personIsIn = False
    if len(list) < 1:
        message += '\nВ этой очереди ещё никто не записан'
    else:
        message += '\n\nСписок:'
        for name in list:
            message += '\n'
            if name == (values.users[id]['name'] + ' ' + values.users[id]['surname']):
                personIsIn = True
                message += '> '
            message += name
    keyboard = getQueueActionsButtons(queue, personIsIn)
    return message, None, keyboard


command = command_system.Command()

command.keys = ['queueActions']
command.description = 'Кнопки для выбора действия в очереди'
command.process = queueActions
