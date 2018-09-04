from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getTimetableButtons
from Bot.Basis.Timetable.getSchedule import getTimetableDict


def showTimetableButtons(values):
    message = 'Выбери день и я пришлю тебе расписание'
    group = [values.users[values.item['from_id']]['group']]
    values.timetableDict.update(getTimetableDict(group))
    keyboard = getTimetableButtons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['showTimetableButtons']
command.description = 'Прислать пользователю кнопки для выбора расписания'
command.process = showTimetableButtons