from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import setToQueue, getQueueList
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons


def addToQueue(values):
    queue = ' '.join(values.message.split(' ')[1:])
    id = int(values.item['from_id'])
    name = values.users[id]['name'] + ' ' + values.users[id]['surname']
    connect = values.connect
    queue_name = '\"' + queue + '\"'
    setToQueue(connect, queue_name, id, name)

    list = getQueueList(connect, queue_name)
    stringList = '\nОчередь на данный момент:'
    for name in list:
        stringList += '\n'
        stringList += name

    message = 'Готово!\n' + stringList
    keyboard = getDefaultScreenButtons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['addToQueue']
command.description = 'Запись или перезапись в очередь'
command.process = addToQueue