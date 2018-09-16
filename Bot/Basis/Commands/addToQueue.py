from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import setToQueue, getQueueList
from Bot.Basis.Keyboards.getButtons import get_default_buttons


def addToQueue(values):
    queue = ' '.join(values.message.split()[1:])
    user_id = int(values.item['from_id'])
    name = values.users[user_id]['name'] + ' ' + values.users[user_id]['surname']
    queue = '\"' + queue + '\"'

    setToQueue(queue, user_id, name)

    message = 'Готово!\nОчередь на данный момент:'
    for name in getQueueList(queue):
        message += '\n'
        if name == (values.users[user_id]['name'] + ' ' + values.users[user_id]['surname']):
            message += '> '
        message += name

    keyboard = get_default_buttons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['addToQueue']
command.description = 'Запись или перезапись в очередь'
command.process = addToQueue
