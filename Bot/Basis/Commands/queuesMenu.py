from Bot.Basis import command_system
from Bot.Basis.Keyboards.getButtons import get_queue_names_buttons, get_default_buttons


def queuesMenu(values):
    message = 'В этом меню показаны доступные тебе очереди. ' \
              'Ты можешь встать в очередь и выйти из неё. Если ты уже есть в очереди, ' \
              'бот предложит тебе встать в конец (допустим, ты уже прошёл и хочешь подойти снова). \n' \
              'Для выбора действия, нажми на кнопку с названием одной из очередей. ' \
              'Так же ты увидишь список людей, которые уже в неё записались.\n\n'

    group = values.users[values.item['from_id']]['group']
    keyboard = get_queue_names_buttons(values.connect, group)

    if keyboard is None:
        message += 'Сейчас доступных для тебя очередей нет =( \n' \
                   'Обратись к старосте или разработчику для открытия новой!'
        keyboard = get_default_buttons(values)
    else:
        message += 'Если в списке ещё нет нужной очереди, обратись к старосте ' \
                   'или разработчику для её открытия)'

    return message, None, keyboard


command = command_system.Command()

command.keys = ['queuesMenu']
command.description = 'Кнопки для выбора очереди (День, предмет)'
command.process = queuesMenu
