from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import removeFromQueueInDB
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons


def removeFromQueue(values):
    queue = values.message.split(' ')[1]
    id = values.item['from_id']
    connect = values.connect

    removed = removeFromQueueInDB(connect, queue, id)
    # TODO: removeFromQueueInDB будет немного проблематично возвращать f/t, поэтому лучше сделать одно сообщение
    if removed:
        message = 'Теперь тебя нет в этой очереди: ' + queue
    else:
        message = 'Тебя в этой очереди и так не было =)'
    keyboard = getDefaultScreenButtons()

    return message, None, keyboard


command = command_system.Command()

command.keys = ['removeFromQueue']
command.description = 'Удаление из очереди'
command.process = removeFromQueue
