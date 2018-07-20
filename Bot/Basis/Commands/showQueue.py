from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getQueueButtons, getDefaultScreenButtons


def showQueue(values):
    queue = values.message.split(' ')[1]
    id = values.item['user_id'] # Может, понадобится, чтоб выделить как-то человека в списке )
    # TODO: функция-работа с БД, которая возвращает список людей в очереди
    message = 'Тут должен быть список людей в очереди' # getQueueList(queue)
    if message == '':
        message = 'В этой очереди ещё никто не записан'
    keyboard = getDefaultScreenButtons()
    return message, None, keyboard


command = command_system.Command()

command.keys = ['showQueue']
command.description = 'Возвращает список выбранной очереди'
command.process = showQueue