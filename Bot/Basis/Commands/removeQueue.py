from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import removeQueueInBD, removeFromDateDeleted, getQueueNames, \
    getDateDeletedTables
from Bot.Basis.Keyboards.getButtons import get_default_buttons
from Bot.Basis.QueueThread import remove_from_asked_list


def removeQueue(values):
    name = ' '.join(values.message.split(' ')[1:])
    name_ = '\"' + name + '\"'

    if name in getQueueNames():
        removeQueueInBD(name_)
        remove_from_asked_list(values.item['from_id'])

    for queue in getDateDeletedTables():
        if name == queue[0]:
            removeFromDateDeleted(name)

    message = 'Удалена очередь: ' + name
    keyboard = get_default_buttons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['removeQueue']
command.description = 'Удаление очереди'
command.process = removeQueue
