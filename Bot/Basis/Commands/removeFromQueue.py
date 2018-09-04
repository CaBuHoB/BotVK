from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import removeFromQueueInDB
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons


def removeFromQueue(values):
    queue = ' '.join(values.message.split(' ')[1:])
    id = values.item['from_id']
    connect = values.connect

    queue_ = '\"' + queue + '\"'
    removeFromQueueInDB(connect, queue_, id)
    message = 'Ты вышел из этой очереди: ' + queue
    keyboard = getDefaultScreenButtons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['removeFromQueue']
command.description = 'Удаление из очереди'
command.process = removeFromQueue
