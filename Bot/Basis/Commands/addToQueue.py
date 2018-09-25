from Bot.Basis import command_system
from Bot.Basis.Functions.workWithDataBase import setToQueue, getQueueList
from Bot.Basis.Functions.getButtons import get_queue_actions_buttons


def addToQueue(values):
    user_id = values.item['from_id']
    name = values.users[user_id]['name'] + ' ' + values.users[user_id]['surname']
    queue = ' '.join(values.message.split()[1:])
    queue_name = '\"' + queue + '\"'

    setToQueue(queue_name, user_id, name)

    message = 'Готово!\n' \
              'Очередь на данный момент:\n'
    for name in getQueueList(queue_name):
        message += '\n'
        if name == (values.users[user_id]['name'] + ' ' + values.users[user_id]['surname']):
            message += '> '
        message += name

    return message, None, get_queue_actions_buttons(queue, True)


command = command_system.Command()

command.keys = ['addToQueue']
command.description = 'Запись или перезапись в очередь'
command.process = addToQueue
