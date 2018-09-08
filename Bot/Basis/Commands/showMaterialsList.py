from Bot.Basis import command_system
from Bot.Basis.Keyboards.getButtons import get_materials_list_buttons


def showMaterialsList(values):
    lesson = values.item['text']
    message = 'Выбери номер лабы и я пришлю тебе файл'
    keyboard = get_materials_list_buttons(lesson, values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['showMaterialsList']
command.description = 'Список материалов по предмету'
command.process = showMaterialsList
