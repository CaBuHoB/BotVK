from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_groups_for_queue_creation_buttons


def queueByDate(values):
    date = values.item['text']
    message = 'Выбери, для каких групп создаётся эта очередь'
    keyboard = get_groups_for_queue_creation_buttons(date, values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['queueByDate']
command.description = 'Выбор групп для очереди'
command.process = queueByDate
