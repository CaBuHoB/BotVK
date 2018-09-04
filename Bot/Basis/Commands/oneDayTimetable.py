from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getTimetableButtons
from Bot.Basis.Timetable.getSchedule import getDate, getTimetableByDay, getDaysForGroup

from datetime import datetime


def oneDayTimetable(values):
    group = values.users[values.item['from_id']]['group']
    isUpper = getDate()['isUpper']
    message_tail = ''

    if (values.item['text'] == 'Сегодня') or (values.item['text'] == 'Завтра'):
        week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        weekdayNumber = datetime.weekday(datetime.now())
        if values.item['text'] == 'Завтра':
            weekdayNumber = (weekdayNumber + 1) % 7
            if weekdayNumber == 0:
                isUpper = not isUpper
        if week[weekdayNumber] in getDaysForGroup(values.timetableDict, group):
            message_tail = getTimetableByDay(values.timetableDict, group, week[weekdayNumber], isUpper)
    else:
        weekday = values.message.split()[1]
        message_tail = getTimetableByDay(values.timetableDict, group, weekday, None)
    if isUpper:
        message = 'Верхняя (красная, нечётная) неделя\n\n'
    else:
        message = 'Нижняя (синяя, чётная) неделя\n\n'
    if message_tail == '':
        message += 'Выходной!)'
    else:
        message += message_tail

    return message, None, getTimetableButtons(values)


command = command_system.Command()

command.keys = ['oneDayTimetable']
command.description = 'Отправка расписания на сегодня или завтра'
command.process = oneDayTimetable