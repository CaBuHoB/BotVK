from Bot.Basis import command_system
from Bot.Basis.Keyboards.getButtons import get_timetable_menu_buttons
from Bot.Basis.Timetable.getSchedule import getTimetableDict


def showTimetableButtons(values):
    message = 'Выбери день и я пришлю тебе расписание. Ты можешь подписаться на рассылку: ' \
              'бот будет присылать расписание на следующий день и уведомлять о начале пар. ' \
              'От неё можно отписаться в любой момент, попробовать стоит ;)'

    group = [values.users[values.item['from_id']]['group']]
    # values.timetableDict.update(getTimetableDict(group))

    keyboard = get_timetable_menu_buttons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['showTimetableButtons']
command.description = 'Прислать пользователю кнопки для выбора расписания'
command.process = showTimetableButtons
