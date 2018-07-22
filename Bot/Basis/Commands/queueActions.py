from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getQueueActionsButtons


def queueActions(values):
    message = 'help по кнопкам в этом меню'
    queue = values.item['body']
    keyboard = getQueueActionsButtons(queue)
    return message, None, keyboard


command = command_system.Command()

command.keys = ['queueActions']
command.description = 'Кнопки для выбора действия в очереди'
command.process = queueActions