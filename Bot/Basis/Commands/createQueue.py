from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import createQueueInBD
from Bot.Basis.Keyboards.getButtons import get_default_buttons, get_dates_for_queue_creation_buttons


def createQueue(values):
    message = 'Выбери дату (можно выбрать дату на пять дней вперед, воскресенья не учитываются)'
    keyboard = get_dates_for_queue_creation_buttons()

    return message, None, keyboard


command = command_system.Command()

command.keys = ['createQueue']
command.description = 'Открытие очереди, выбор даты'
command.process = createQueue
