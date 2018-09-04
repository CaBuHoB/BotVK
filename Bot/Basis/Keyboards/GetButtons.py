import json
from enum import Enum
from datetime import datetime, timedelta

from Bot.Basis.DataBase.workWithDataBase import getQueueNames, getSubjects, getSubscribedUsers
from Bot.Basis.Timetable.getSchedule import getDaysDict, getDaysForGroup
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


def getDefaultScreenButtons(values=None, id=None):
    queueButtons = [getButton('Очередь', 'queuesMenu', Color.WHITE)]
    infoMessageButton = None

    if values is not None:
        user_id = values.item['from_id'] if id is None else id
        surname = values.users[user_id]['surname']
        if (surname == 'Борисова'): #(surname == 'Савинов') or
            queueButtons.append(getButton('Создать очередь', 'createQueue', Color.WHITE))
            infoMessageButton = [getButton('Рассылка', 'infoMessage', Color.WHITE)]

    listOfButtons = []
    listOfButtons.append([
        getButton('Материалы', 'materialsMenu', Color.WHITE),
        getButton('Решение задач', 'kroukMenu', Color.WHITE)
    ])
    listOfButtons.append(queueButtons)
    listOfButtons.append([getButton('Расписание', 'showTimetableButtons', Color.WHITE)])
    listOfButtons.append(infoMessageButton) if infoMessageButton is not None else None
    listOfButtons.append([getButton('?', 'help', Color.GREEN)])

    return json.dumps({
        "one_time": False,
        "buttons": listOfButtons
    }, ensure_ascii=False)


def getButtonsWithGroups():
    groupsList = getGroupNumbersFromGoogle()
    if len(groupsList) == 0:
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


def getQueueButtons(connect, group):
    queues = getQueueNames(connect)
    queueList = []
    for queue in queues:
        groupsList = (queue.split('_')[1]).split()
        if str(group) in groupsList:
            queueList.append(queue)
    if len(queueList) == 0:
        return None

    buttonsList = [[getButton(queue, 'queueActions', Color.BLUE)] for queue in queueList]
    buttonsList.append([getButton('⟵ в главное меню', 'backToDefaultKeyboard', Color.WHITE)])
    return json.dumps({
        "one_time": False,
        "buttons": buttonsList
    }, ensure_ascii=False)


def getQueueActionsButtons(queue, personIsIn):
    if personIsIn:
        buttons = [getButton('Встать в конец очереди', 'addToQueue ' + queue, Color.WHITE),
                getButton('Выйти из очереди', 'removeFromQueue ' + queue, Color.WHITE)]
    else:
        buttons = [getButton('Встать в очередь', 'addToQueue ' + queue, Color.WHITE)]

    return json.dumps({
        "one_time": False,
        "buttons": [
            buttons,
            [
                getButton('⟵ к списку очередей', 'queuesMenu', Color.BLUE),
            ],
            [
                getButton('⟵ в главное меню', 'backToDefaultKeyboard', Color.BLUE),
            ]
        ]
    }, ensure_ascii=False)


def getMaterialsActionsButtons(values):
    items = values.vkApi.method('docs.search', {'q': '>', 'search_own': 1, 'count': 200})['items']
    materialsList = []
    for doc in items:
        if doc['owner_id'] == -168366525:
            # TODO: заменить id тестовой группы на число основной
            materialsList.append(doc['title'])
    if len(materialsList) == 0:
        return None

    subjectsList = []
    for material in materialsList:
        subject = material.split()[1]
        if not subject in subjectsList:
            subjectsList.append(subject)

    buttonsList = [[getButton(subject, 'showMaterialsList', Color.WHITE)] for subject in subjectsList]
    buttonsList.append([getButton('⟵ в главное меню', 'backToDefaultKeyboard', Color.BLUE)])
    return json.dumps({
        "one_time": False,
        "buttons": buttonsList
    }, ensure_ascii=False)


def getMaterialsListButtons(subject, values):
    items = values.vkApi.method('docs.search', {'q': '>', 'search_own': 1, 'count': 200})['items']
    materialsList = []
    for doc in items:
        if (doc['owner_id'] == -168366525) and (doc['title'].split()[1] == subject):
            # TODO: заменить id тестовой группы на число основной
            materialsList.append(doc['title'])

    buttonsList = [[getButton(material.split()[2], 'getFile ' + material, Color.WHITE)] \
                     for material in materialsList]
    buttonsList.append([getButton('⟵ в меню материалов', 'materialsMenu', Color.BLUE),
                          getButton('⟵ в главное меню', 'backToDefaultKeyboard', Color.BLUE)])
    return json.dumps({
        "one_time": False,
        "buttons": buttonsList
    }, ensure_ascii=False)


def getDatesButtons():
    week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
    date = datetime.now()
    weekday = datetime.weekday(date)
    daysList = []
    for i in range(5):
        if weekday == 6: # Пропуск воскресенья
            date += timedelta(1)
            weekday = 0
        day_str = str(date.timetuple()[2])
        month = date.timetuple()[1]
        month_str = str(month)
        if (month - 10) < 0:
            month_str = '0' + month_str
        daysList.append(day_str + '.' + month_str + ' (' + week[weekday] + ')')
        date += timedelta(1)
        weekday += 1

    buttonsList = [[getButton(day, 'queueByDate', Color.BLUE)] for day in daysList]
    buttonsList.append([getButton('⟵ в главное меню', 'backToDefaultKeyboard', Color.RED)])

    return json.dumps({
        "one_time": False,
        "buttons": buttonsList
    }, ensure_ascii=False)


def getGroupsForQueueButtons(date):
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                getButton('5621', 'queueByGroup ' + date, Color.BLUE),
                getButton('5622', 'queueByGroup ' + date, Color.BLUE),
                getButton('5623', 'queueByGroup ' + date, Color.BLUE)
            ],
            [
                getButton('5621 5622', 'queueByGroup ' + date, Color.BLUE),
                getButton('5621 5623', 'queueByGroup ' + date, Color.BLUE),
                getButton('5622 5623', 'queueByGroup ' + date, Color.BLUE)
            ],
            [
                getButton('5621 5622 5623', 'queueByGroup ' + date, Color.BLUE)
            ],
            [
                getButton('⟵ к выбору даты', 'createQueue', Color.RED),
                getButton('⟵ в главное меню', 'backToDefaultKeyboard', Color.RED)
            ]
        ]
    }, ensure_ascii=False)


def getSubjectsForQueueButtons(values, tail_of_queue_name):
    subList = getSubjects(values.connect)
    if len(subList) == 0:
        return None

    buttonsList = []
    twoButtonsList = []
    for sub in subList:
        twoButtonsList.append(sub)
        if len(twoButtonsList) == 2:
            buttonsList.append(twoButtonsList)
            twoButtonsList = []
    if len(twoButtonsList) != 0:
        buttonsList.append(twoButtonsList)

    buttonsList = [[getButton(sub, 'queueCteation ' + tail_of_queue_name, Color.BLUE)
                    for sub in twoButtonsList] for twoButtonsList in buttonsList]
    buttonsList.append([
                getButton('⟵ к выбору группы', 'queueByDate', Color.RED),
                getButton('⟵ в главное меню', 'backToDefaultKeyboard', Color.RED)
            ])

    return json.dumps({
        "one_time": False,
        "buttons": buttonsList
    }, ensure_ascii=False)


def getGroupsForMessageButtons():
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                getButton('5621', 'infoByGroup', Color.BLUE),
                getButton('5622', 'infoByGroup', Color.BLUE),
                getButton('5623', 'infoByGroup', Color.BLUE)
            ],
            [
                getButton('5621 5622', 'infoByGroup', Color.BLUE),
                getButton('5621 5623', 'infoByGroup', Color.BLUE),
                getButton('5622 5623', 'infoByGroup', Color.BLUE)
            ],
            [
                getButton('5621 5622 5623', 'infoByGroup', Color.BLUE)
            ],
            [
                getButton('⟵ Отмена', 'backToDefaultKeyboard', Color.RED)
            ]
        ]
    }, ensure_ascii=False)


def getMessageEscapeButton():
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                getButton('⟵ Отмена', 'backToDefaultKeyboard', Color.RED)
            ]
        ]
    }, ensure_ascii=False)


def getSendOrNoButtons():
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                getButton('Разослать', 'infoSendMessage', Color.GREEN)
            ],
            [
                getButton('⟵ Отмена', 'backToDefaultKeyboard', Color.RED)
            ]
        ]
    }, ensure_ascii=False)


def getMaterialsActionsButtons(values):
    items = values.vkApi.method('docs.search', {'q': '>', 'search_own': 1, 'count': 200})['items']
    materialsList = []
    for doc in items:
        if doc['owner_id'] == -168330527:  # -168366525:  # TODO: заменить id тестовой группы на число основной
            materialsList.append(doc['title'])
    if len(materialsList) == 0:
        return None


def queueDeleteButtons(queue):
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                getButton('Удалить очередь', 'removeQueue ' + queue, Color.RED)
            ],
            [
                getButton('Перенести удаление на три дня', 'rewriteQueueDelete ' + queue, Color.RED)
            ]
        ]
    }, ensure_ascii=False)


def getTimetableButtons(values):
    id = values.item['from_id']
    group = values.users[id]['group']

    if id not in getSubscribedUsers(values.connect):
        subscribeButton = [getButton('Подписаться на рассылку', 'timetableSending sub', Color.GREEN)]
    else:
        subscribeButton = [getButton('Отписаться от рассылки', 'timetableSending unsub', Color.RED)]

    daysDict = getDaysDict()
    daysList = []
    for day in daysDict:
        if day in getDaysForGroup(values.timetableDict, group):
            daysList.append(day)
    threeButtonsList = []
    buttonsList = []
    for day in daysList:
        buttonsList.append(day)
        if len(buttonsList) == 3:
            threeButtonsList.append(buttonsList)
            buttonsList = []
    if len(buttonsList) != 0:
        threeButtonsList.append(buttonsList)

    listOfButtons = [[getButton('Сегодня', 'oneDayTimetable', Color.WHITE),
                getButton('Завтра', 'oneDayTimetable', Color.WHITE)]]
    for daysList in threeButtonsList:
        listOfButtons.append([getButton(daysDict[day], 'oneDayTimetable ' + day, Color.BLUE)
                   for day in daysList])
    listOfButtons.append([getButton('На всю неделю', 'askTheWeek', Color.WHITE)])
    listOfButtons.append(subscribeButton)
    listOfButtons.append([getButton('⟵ В главное меню', 'backToDefaultKeyboard', Color.BLUE)])

    return json.dumps({
        "one_time": False,
        "buttons": listOfButtons
    }, ensure_ascii=False)


def getAskingWeekButtons():
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                getButton('Текущая', 'fullWeekTimetable', Color.WHITE),
                getButton('Следующая', 'fullWeekTimetable', Color.WHITE),
                getButton('Полное расписание', 'fullWeekTimetable', Color.WHITE)
            ],
            [
                getButton('⟵ В меню расписания', 'showTimetableButtons', Color.BLUE),
                getButton('⟵ В главное меню', 'backToDefaultKeyboard', Color.BLUE)
            ]
        ]
    }, ensure_ascii=False)
