from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import createQueueInBD
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons, getDatesButtons


def createQueue(values):

    message = 'Выбери дату (можно выбрать дату на пять дней вперед, воскресенья не учитываются)'
    keyboard = getDatesButtons()

    return message, None, keyboard


command = command_system.Command()

command.keys = ['createQueue']
command.description = 'Открытие очереди, выбор даты'
command.process = createQueue
