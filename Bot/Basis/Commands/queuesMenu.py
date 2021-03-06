from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_queue_names_buttons, get_default_buttons


def queuesMenu(values):
    message = 'В этом меню показаны все открытые очереди. ' \
              'Ты можешь встать в очередь, доступную для твоей группы, и выйти из неё. ' \
              'Если ты уже есть в очереди, бот предложит тебе встать в конец ' \
              '(допустим, ты уже прошёл и хочешь подойти снова). \n' \
              'Для выбора действия, нажми на кнопку с названием одной из очередей. ' \
              'Так же ты увидишь список людей, которые уже в неё записались.\n\n'

    keyboard = get_queue_names_buttons()

    if keyboard is None:
        message += 'Сейчас доступных очередей нет =( \n' \
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
