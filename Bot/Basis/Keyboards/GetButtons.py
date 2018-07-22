import json
from enum import Enum

from Bot.Basis.YandexGoogle.GoogleTables import getNamesListFromGoogle, getGroupNumbersFromGoogle


class Color(Enum):
    RED = 'negative'
    GREEN = 'positive'
    WHITE = 'default'
    BLUE = 'primary'


def getButton(label, payload, color=Color.WHITE):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload, ensure_ascii=False),
            "label": label
        },
        "color": color.value
    }


def getButtonsWithGroups():
    groupsList = getGroupNumbersFromGoogle()
    if groupsList is None:
        return None

    buttonsList = [[getButton(group, 'showNamesList', Color.BLUE)] for group in groupsList]
    return json.dumps({
        "one_time": True,
        "buttons": buttonsList
    }, ensure_ascii=False)


def getButtonsWithNames(group):
    namesList = getNamesListFromGoogle(group)
    if len(namesList) == 0:
        return None

    buttonsList = []
    twoButtonsList = []
    for name in namesList:
        twoButtonsList.append(name)
        if len(twoButtonsList) == 2:
            buttonsList.append(twoButtonsList)
            twoButtonsList = []
    if len(twoButtonsList) != 0:
        buttonsList.append(twoButtonsList)

    buttonsList = [[getButton(button, 'endOfRegistration ' + group, Color.BLUE)
                    for button in twoButtonsList] for twoButtonsList in buttonsList]

    return json.dumps({
        "one_time": True,
        "buttons": buttonsList
    }, ensure_ascii=False)


def getDefaultScreenButtons():
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                getButton('Материалы', 'materialsMenu', Color.WHITE),
                getButton('Решение задач', 'kroukMenu', Color.WHITE)
            ],
            [
                getButton('Очередь', 'queuesMenu', Color.WHITE)
            ],
            [
                getButton('?', 'help', Color.GREEN)
            ]
        ]
    }, ensure_ascii=False)


def getQueueButtons(user_id):
    # TODO: getQueueNames(user_id) - возвращает список [] строк с названиями очередей из БД.
    # Только те очереди, которые доступны человеку определенной группы по user_id

    buttonsList = []  # getQueueNames()

    if len(buttonsList) == 0:
        return None

    listOfButtons = [[getButton(but, 'queueActions', Color.BLUE)] for but in buttonsList]
    listOfButtons.append([getButton('⟵', 'backToDefaultKeyboard', Color.WHITE)])
    return json.dumps({
        "one_time": True,
        "buttons": listOfButtons
    }, ensure_ascii=False)


def getQueueActionsButtons(queue):
    return json.dumps({
        "one_time": True,
        "buttons": [
            [
                getButton('Встать в очередь', 'addToQueue ' + queue, Color.WHITE),
                getButton('Выйти из очереди', 'removeFromQueue ' + queue, Color.WHITE)
            ],
            [
                getButton('Показать список', 'showQueue ' + queue, Color.WHITE)
            ],
            [
                getButton('⟵', 'backToDefaultKeyboard', Color.BLUE),
            ]
        ]
    }, ensure_ascii=False)


def getAlreadyInQueueButtons(queue):
    return json.dumps({
        "one_time": True,
        "buttons": [
            [
                getButton('Встать в конец', 'addToQueue ' + queue, Color.WHITE)
            ],
            [
                getButton('⟵', 'backToDefaultKeyboard', Color.WHITE)
            ]
        ]
    }, ensure_ascii=False)


def getTestButtons():
    return json.dumps({
        "one_time": True,
        "buttons": [
            [
                getButton('⟵', 'backToDefaultKeyboard', Color.RED)
            ]
        ]
    }, ensure_ascii=False)


# TODO: Добавить команды showLabList и showConspectsList
# Это работа с файлами, там не знаю, делать кнопки или текстом людям будет проще написать
# Пока что вместо этих кнопок используется getTestButtons()
def getMaterialsActionsButtons():
    return json.dumps({
        "one_time": True,
        "buttons": [
            [
                getButton('Лабы', 'showLabList', Color.WHITE),
                getButton('Билеты/Конспекты', 'showConspectsList', Color.WHITE)
            ],
            [
                getButton('⟵', 'setStartScreenButtons', Color.WHITE)
            ]
        ]
    }, ensure_ascii=False)

# TODO: Сделать выход не только в главное меню, но и на одну клавиатуру назад
