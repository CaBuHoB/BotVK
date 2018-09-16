from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import subscribePerson, unSubscribePerson
from Bot.Basis.Keyboards.getButtons import get_timetable_menu_buttons


def timetableSending(values):
    if values.message.split()[1] == 'sub':
        subscribePerson(values.item['from_id'])
        message = 'Ты подписался на рассылку.\n' \
                  'В 21:00 тебе будет приходить расписание на следующий день.\n' \
                  'За 15 минут до начала каждой пары будет приходить уведомление с информацией. ' \
                  'В любой момент ты можешь отписаться, нажав на красную кнопку в меню расписания)'
    else:
        unSubscribePerson(values.item['from_id'])
        message = 'Ты отписался от рассылки расписания'

    return message, None, get_timetable_menu_buttons(values)


command = command_system.Command()

command.keys = ['timetableSending']
command.description = 'Подписка/Отписка рассылки'
command.process = timetableSending
