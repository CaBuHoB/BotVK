from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getTestButtons


def materialsMenu(values):
    # TODO изменить метод, сделать сразу нормально. Можно подргужать снова данные из google drive
    message = 'Материалов пока нет =(\n' \
              'Если хочешь внести свою лепту - напиши админу!)'
    keyboard = getTestButtons()
    return message, None, keyboard


command = command_system.Command()

command.keys = ['materialsMenu']
command.description = 'Меню материалов'
command.process = materialsMenu

