from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons


def removeFromQueue(values):
    queue = values.message.split(' ')[1]
    id = values.item['user_id']

    # TODO: boolean выкидывание из очереди в БД. True, если он там был, False, и так не было
    # removeFromQueue(queue, id)
    removeFromQueue = True

    if removeFromQueue:
        message = 'Теперь тебя нет в этой очереди: ' + queue
    else:
        message = 'Тебя там и не было =)' # + Показать человеку очередь
    keyboard = getDefaultScreenButtons()

    return message, None, keyboard


command = command_system.Command()

command.keys = ['removeFromQueue']
command.description = 'Удаление из очереди'
command.process = removeFromQueue