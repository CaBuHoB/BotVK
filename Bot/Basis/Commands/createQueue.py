from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons


# Надо имя посложнее, чтоб доступ был не у всех
def createQueue(values):
    name = values.message.split(' ')[1]
    connect = values.connect
    # TODO: createQueueInBD(connect, name) для создания очереди из диалога с ботом
    message = 'Очередь создана'
    keyboard = getDefaultScreenButtons()
    return message, None, keyboard


command = command_system.Command()

command.keys = ['createQueue']
command.description = 'Открытие очереди'
command.process = createQueue