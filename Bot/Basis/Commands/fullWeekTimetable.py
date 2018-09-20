from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_timetable_menu_buttons
from Bot.Basis.Functions.getSchedule import getTimetableByWeek


def fullWeekTimetable(values):
    group = values.users[values.item['from_id']]['group']
    message = ''

    isUpper = None
    if values.item['text'] == 'Текущая':
        isUpper = values.isUpper
    elif values.item['text'] == 'Следующая':
        isUpper = not values.isUpper

    if isUpper:
        message = 'Сейчас верхняя (красная, нечётная) неделя\n\n'
    elif not isUpper:
        message = 'Сейчас нижняя (синяя, чётная) неделя\n\n'

    message += getTimetableByWeek(values.timetableDict, group, isUpper)

    return message, None, get_timetable_menu_buttons(values)


command = command_system.Command()

command.keys = ['fullWeekTimetable']
command.description = 'Отправка расписания на полную неделю'
command.process = fullWeekTimetable
