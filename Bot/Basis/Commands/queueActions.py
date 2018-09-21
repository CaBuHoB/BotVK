from Bot.Basis import command_system
from Bot.Basis.Functions.workWithDataBase import getQueueList
from Bot.Basis.Functions.getButtons import get_queue_actions_buttons


def queueActions(values):
    user_id = values.item['from_id']
    queue = values.item['text']
    if queue == '⟵ в меню этой очереди':
        queue = values.message.split()[1]

    queue_list = getQueueList('\"' + queue + '\"')
    message = 'Название очереди: ' + queue
    person_is_in = False

    if len(queue_list) < 1:
        message += '\nВ этой очереди никто не записан'
    else:
        message += '\n\nСписок:'
        for name in queue_list:
            message += '\n'
            if name == (values.users[user_id]['name'] + ' ' + values.users[user_id]['surname']):
                person_is_in = True
                message += '> '
            message += name

    if str(values.users[user_id]['group']) not in (queue.split('_')[1]).split():
        if len((queue.split('_')[1]).split()) > 1:
            message += '\n\nЭта очередь доступна тебе только для просмотра, так как она' \
                       ' была создана для других групп'
        else:
            message += '\n\nЭта очередь доступна тебе только для просмотра, так как она' \
                       ' была создана для другой группы'
        return message, None, None

    keyboard = get_queue_actions_buttons(queue, person_is_in)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['queueActions']
command.description = 'Кнопки для выбора действия в очереди'
command.process = queueActions
