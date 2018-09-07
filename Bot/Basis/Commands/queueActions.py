from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import getQueueList
from Bot.Basis.Keyboards.getButtons import get_queue_actions_buttons


def queueActions(values):
    user_id = values.item['from_id']
    queue = values.item['text']
    if queue == '⟵ в меню этой очереди':
        queue = values.message.split()[1]

    connect = values.connect
    queue_list = getQueueList(connect, ('\"' + queue + '\"'))
    message = 'Название очереди: ' + queue
    personIsIn = False

    if len(queue_list) < 1:
        message += '\nВ этой очереди ещё никто не записан'
    else:
        message += '\n\nСписок:'
        for name in queue_list:
            message += '\n'
            if name == (values.users[user_id]['name'] + ' ' + values.users[user_id]['surname']):
                personIsIn = True
                message += '> '
            message += name

    keyboard = get_queue_actions_buttons(queue, personIsIn)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['queueActions']
command.description = 'Кнопки для выбора действия в очереди'
command.process = queueActions
