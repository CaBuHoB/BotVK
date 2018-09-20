from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_timetable_menu_buttons
from Bot.Basis.Functions.getSchedule import getTimetableByDay, getDaysForGroup

from datetime import datetime


def oneDayTimetable(values):
    group = values.users[values.item['from_id']]['group']
    isUpper = values.isUpper
    message_tail = ''

    if (values.item['text'] == 'Сегодня') or (values.item['text'] == 'Завтра'):
        week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        weekday_number = datetime.weekday(datetime.now())

        if values.item['text'] == 'Завтра':
            weekday_number = (weekday_number + 1) % 7
            if weekday_number == 0:
                isUpper = not isUpper

        if week[weekday_number] in getDaysForGroup(values.timetableDict, group):
            message_tail = getTimetableByDay(values.timetableDict, group, week[weekday_number], isUpper)
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

    return message, None, get_timetable_menu_buttons(values)


command = command_system.Command()

command.keys = ['oneDayTimetable']
command.description = 'Отправка расписания на сегодня или завтра'
command.process = oneDayTimetable
