from Bot.Basis import command_system
from Bot.Basis.Functions.workWithDataBase import getSubscribedUsers
from Bot.Basis.Functions.getButtons import get_timetable_menu_buttons


def showTimetableButtons(values):
    message = 'Выбери день и я пришлю тебе расписание' \
              ''
    if values.item['from_id'] not in getSubscribedUsers():
        message += '\n\nТы можешь подписаться на рассылку: ' \
                   'бот будет присылать расписание на следующий день и уведомлять о начале пар. ' \
                   'От неё можно отписаться в любой момент, попробовать стоит ;)'

    keyboard = get_timetable_menu_buttons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['showTimetableButtons']
command.description = 'Прислать пользователю кнопки для выбора расписания'
command.process = showTimetableButtons
