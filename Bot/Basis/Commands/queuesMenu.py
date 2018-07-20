from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getQueueButtons, getDefaultScreenButtons


def queuesMenu(values):
    message = 'Выбери дату и предмет. Если в списке ещё нет нужной очереди, обратись к старосте ' \
              'или разработчикам для её открытия'
    id = values.item['user_id']
    keyboard = getQueueButtons(id)
    if keyboard is None:
        message = 'Сейчас доступных очередей нет =( \n' \
                  'Обратись к старосте или разработчикам для открытия новой!'
        keyboard = getDefaultScreenButtons()
    return message, None, keyboard


command = command_system.Command()

command.keys = ['queuesMenu']
command.description = 'Кнопки для выбора очереди (День, предмет)'
command.process = queuesMenu