from datetime import datetime, timedelta
from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import removeQueueInBD, updateDateInDateDeleted
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons


def rewriteQueueDelete(values):
    name = values.message.split(' ')[1:]
    name = ' '.join(name)

    new_date = datetime.now() + timedelta(3)
    day = str(new_date.timetuple()[2])
    month = str(new_date.timetuple()[1])
    year = str(new_date.timetuple()[0])
    date = day + '.' + month + '.' + year

    name_ = '\"' + name + '\"'
    updateDateInDateDeleted(values.connect, name_, date)

    message = 'Перенесена дата удаления очереди ' + name
    keyboard = getDefaultScreenButtons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['rewriteQueueDelete']
command.description = 'Перенос даты удаления очереди'
command.process = rewriteQueueDelete