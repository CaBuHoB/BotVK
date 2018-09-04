from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import removeQueueInBD, removeFromDateDeleted, getQueueNames, \
    getDateDeletedTables
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons


def removeQueue(values):
    name = values.message.split(' ')[1:]
    name = ' '.join(name)
    n = '\"' + name + '\"'

    if name in getQueueNames(values.connect):
        removeQueueInBD(values.connect, n)
    for queue in getDateDeletedTables(values.connect):
        if name == queue[0]:
            removeFromDateDeleted(values.connect, name)
    if name in values.appealsForQueueDelete:
        values.appealsForQueueDelete.remove(name)

    message = 'Удалена очередь: ' + name
    keyboard = getDefaultScreenButtons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['removeQueue']
command.description = 'Удаление очереди'
command.process = removeQueue