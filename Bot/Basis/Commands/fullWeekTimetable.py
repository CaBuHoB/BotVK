from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getTimetableButtons
from Bot.Basis.Timetable.getSchedule import getDate, getTimetableByWeek


def fullWeekTimetable(values):
    group = values.users[values.item['from_id']]['group']
    isUpper = None
    message = ''
    if values.item['text'] == 'Текущая':
        isUpper = getDate()['isUpper']
    elif values.item['text'] == 'Следующая':
        isUpper = not getDate()['isUpper']

    if isUpper == True:
        message = 'Сейчас верхняя (красная, нечётная) неделя\n\n'
    elif isUpper == False:
        message = 'Сейчас нижняя (синяя, чётная) неделя\n\n'
    message += getTimetableByWeek(values.timetableDict, group, isUpper)

    return message, None, getTimetableButtons(values)


command = command_system.Command()

command.keys = ['fullWeekTimetable']
command.description = 'Отправка расписания на полную неделю'
command.process = fullWeekTimetable