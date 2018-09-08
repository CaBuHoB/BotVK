from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import getSubscribedUsers
from Bot.Basis.Keyboards.getButtons import get_timetable_menu_buttons
from Bot.Basis.Timetable.getSchedule import getTimetableDict


def showTimetableButtons(values):
    message = 'Выбери день и я пришлю тебе расписание' \
              ''
    if values.item['from_id'] not in getSubscribedUsers(values.connect):
        message += '\n\nТы можешь подписаться на рассылку: ' \
                   'бот будет присылать расписание на следующий день и уведомлять о начале пар. ' \
                   'От неё можно отписаться в любой момент, попробовать стоит ;)'

    keyboard = get_timetable_menu_buttons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['showTimetableButtons']
command.description = 'Прислать пользователю кнопки для выбора расписания'
command.process = showTimetableButtons
