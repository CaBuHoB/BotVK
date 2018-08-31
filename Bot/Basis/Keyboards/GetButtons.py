import json
from enum import Enum

from Bot.Basis.DataBase.workWithDataBase import getQueueNames
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
    buttonsList.append([getButton('⟵', 'errorInGroupChoosing', Color.RED)])

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


def getQueueButtons(connect, group_number):

    buttonsList = getQueueNames(connect) #возвращает список [] строк с названиями очередей из БД
    newButtonsList = []
    for button in buttonsList:
        groups = button.split('_')[1]
        groupsList = groups.split(' ')
        for group in groupsList:
            if group == group_number:
               newButtonsList.append(button)

    if len(newButtonsList) == 0:
        return None

    listOfButtons = [[getButton(but, 'queueActions', Color.BLUE)] for but in newButtonsList]
    listOfButtons.append([getButton('⟵ в главное меню', 'backToDefaultKeyboard', Color.WHITE)])
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
                getButton('⟵ к списку очередей', 'queuesMenu', Color.BLUE),
            ],
            [
                getButton('⟵ в главное меню', 'backToDefaultKeyboard', Color.BLUE),
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
                getButton('⟵ в меню этой очереди', 'queueActions ' + queue, Color.BLUE),
                getButton('⟵ в меню всех очередей', 'queuesMenu', Color.BLUE)
            ],
            [
                getButton('⟵ в главное меню', 'backToDefaultKeyboard', Color.BLUE)
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


def getMaterialsActionsButtons(values):
    materialsList = []
    docs = values.vkApi.method('docs.search', {'q': '_', 'search_own': 1, 'count': 100})['items']
    for doc in docs:
        materialsList.append(doc['title'])

    if len(materialsList) == 0:
        return None

    lessonsList = []
    for material in materialsList:
        lesson = material.split('_')[0]
        if not lesson in lessonsList:
            lessonsList.append(lesson)

    listOfButtons = [[getButton(lesson, 'showMaterialsList', Color.WHITE)] for lesson in lessonsList]
    listOfButtons.append([getButton('⟵ в главное меню', 'backToDefaultKeyboard', Color.BLUE)])
    return json.dumps({
        "one_time": False,
        "buttons": listOfButtons
    }, ensure_ascii=False)

def getMaterialsListButtons(lessonName, values):
    materialsList = []
    docs = values.vkApi.method('docs.search', {'q': '_', 'search_own': 1, 'count': 100})['items']
    for doc in docs:
        materialsList.append(doc['title'])

    neededMaterialsList = []
    for material in materialsList:
        lesson = material.split('_')[0]
        if lesson == lessonName:
            neededMaterialsList.append(material)

    listOfButtons = [[getButton(material.split('_')[1], 'getFile ' + material, Color.WHITE)]
                     for material in neededMaterialsList]
    listOfButtons.append([getButton('⟵ в меню материалов', 'materialsMenu', Color.BLUE),
                          getButton('⟵ в главное меню', 'backToDefaultKeyboard', Color.BLUE)])
    return json.dumps({
        "one_time": False,
        "buttons": listOfButtons
    }, ensure_ascii=False)