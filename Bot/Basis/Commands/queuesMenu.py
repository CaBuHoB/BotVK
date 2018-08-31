from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getQueueButtons, getDefaultScreenButtons


def queuesMenu(values):
    message = 'Выбери дату и предмет. Если в списке ещё нет нужной очереди, обратись к старосте ' \
              'или разработчику для её открытия'
    id = values.item['from_id']
    person = values.users[id]
    group = person['group']
    keyboard = getQueueButtons(values.connect, group)
    if keyboard is None:
        message = 'Сейчас доступных для тебя очередей нет =( \n' \
                  'Обратись к старосте или разработчику для открытия новой!'
        keyboard = getDefaultScreenButtons()
    return message, None, keyboard


command = command_system.Command()

command.keys = ['queuesMenu']
command.description = 'Кнопки для выбора очереди (День, предмет)'
command.process = queuesMenu