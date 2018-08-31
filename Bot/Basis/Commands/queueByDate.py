from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getGroupsForQueueButtons


def queueByDate(values):
    date = values.item['text']
    message = 'Выбери, для каких групп эта очередь'
    keyboard = getGroupsForQueueButtons(date)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['queueByDate']
command.description = 'Выбор групп для очереди'
command.process = queueByDate