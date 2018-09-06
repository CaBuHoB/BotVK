from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import removeFromQueueInDB
from Bot.Basis.Keyboards.getButtons import get_default_buttons


def removeFromQueue(values):
    queue = ' '.join(values.message.split(' ')[1:])
    user_id = values.item['from_id']

    message = 'Ты вышел из этой очереди: ' + queue
    keyboard = get_default_buttons(values)
    queue = '\"' + queue + '\"'
    removeFromQueueInDB(values.connect, queue, user_id)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['removeFromQueue']
command.description = 'Удаление из очереди'
command.process = removeFromQueue
