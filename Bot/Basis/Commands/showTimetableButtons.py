from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_timetable_menu_buttons


def showTimetableButtons(values):
    message = 'Выбери день и я пришлю тебе расписание'
    keyboard = get_timetable_menu_buttons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['showTimetableButtons']
command.description = 'Прислать пользователю кнопки для выбора расписания'
command.process = showTimetableButtons
