import calendar
import json
from enum import Enum
import datetime as dt
from datetime import datetime, timedelta

from Bot.Basis.DataBase.workWithDataBase import getQueueNames, getSubjects, getSubscribedUsers
from Bot.Basis.QueueThread import in_asked_list
from Bot.Basis.Timetable.getSchedule import getDaysForGroup
from Bot.Basis.YandexGoogle.GoogleTables import getNamesListFromGoogle, getGroupNumbersFromGoogle


class Color(Enum):
    RED = 'negative'
    GREEN = 'positive'
    WHITE = 'default'
    BLUE = 'primary'


def get_button(label, payload, color=Color.WHITE):
    return {
        "action": {"type": "text",
                   "payload": json.dumps(payload, ensure_ascii=False),
                   "label": label},
        "color": color.value
    }


def get_default_buttons(values, users_id=None):
    user_id = values.item['from_id'] if users_id is None else users_id
    if in_asked_list(user_id) or user_id not in values.users:
        return None
    queue_buttons = [get_button('Очередь', 'queuesMenu', Color.WHITE)]
    info_message_button = None

    surname = values.users[user_id]['surname']
    if (surname == 'Савинов') or (surname == 'Ялышев') or \
            (surname == 'Мусикян') or (surname == 'Наумов') or \
            (surname == 'Борисова') or (surname == 'Патерикина'):
        queue_buttons.append(get_button('Создать очередь', 'createQueue', Color.WHITE))
        info_message_button = [get_button('Рассылка сообщений', 'infoMessage', Color.WHITE)]

    buttons_list = []
    buttons_list.append([
        get_button('Лабы и материалы', 'materialsMenu', Color.WHITE),
        get_button('Алгоритмы', 'kroukMenu', Color.WHITE)
    ])
    buttons_list.append(queue_buttons)
    buttons_list.append([get_button('Расписание', 'showTimetableButtons', Color.WHITE)])
    buttons_list.append(info_message_button) if info_message_button is not None else None
    buttons_list.append([get_button('?', 'help', Color.GREEN)])

    return json.dumps({
        "one_time": False,
        "buttons": buttons_list
    }, ensure_ascii=False)


def get_choose_group_buttons():
    buttons_list = [[get_button(group, 'showNamesList', Color.BLUE)]
                    for group in getGroupNumbersFromGoogle()]

    if len(buttons_list) == 0:
        return None

    return json.dumps({
        "one_time": True,
        "buttons": buttons_list
    }, ensure_ascii=False)


def get_choose_name_buttons(group):
    buttons_list = []
    two_buttons_pack = []
    for name in getNamesListFromGoogle(group):
        two_buttons_pack.append(name)
        if len(two_buttons_pack) == 2:
            buttons_list.append(two_buttons_pack)
            two_buttons_pack = []
    if len(two_buttons_pack) != 0:
        buttons_list.append(two_buttons_pack)
    if len(buttons_list) == 0:
        return None

    buttons_list = [[get_button(button, 'endOfRegistration ' + group, Color.BLUE)
                     for button in two_buttons_pack]
                    for two_buttons_pack in buttons_list]
    buttons_list.append([get_button('⟵', 'errorInGroupChoosing', Color.RED)])

    return json.dumps({
        "one_time": True,
        "buttons": buttons_list
    }, ensure_ascii=False)


def get_queue_names_buttons(connect, group):
    queue_list = []
    for queue in getQueueNames(connect):
        now = datetime.now()

        queue_date = queue.split('_')[2].split()[0].split('.')
        day = int(queue_date[0])
        month = int(queue_date[1])
        invisible_time = dt.datetime(now.timetuple()[0], month, day, 23, 0)

        if (invisible_time - now).days > 200:
            invisible_time -= timedelta(366 if calendar.isleap(now.timetuple()[0] - 1) else 365)
        if (now - invisible_time).days < 0:
            queue_list.append(queue)

    if len(queue_list) == 0:
        return None

    buttons_list = [[get_button(queue, 'queueActions', Color.BLUE)] for queue in queue_list]
    buttons_list.append([get_button('⟵ главное меню', 'backToDefaultKeyboard', Color.WHITE)])

    return json.dumps({
        "one_time": False,
        "buttons": buttons_list
    }, ensure_ascii=False)


def get_queue_actions_buttons(queue, person_is_in):
    if person_is_in:
        buttons = [get_button('Встать в конец', 'addToQueue ' + queue, Color.WHITE),
                   get_button('Выйти из очереди', 'removeFromQueue ' + queue, Color.WHITE)]
    else:
        buttons = [get_button('Встать в очередь', 'addToQueue ' + queue, Color.WHITE)]

    return json.dumps({
        "one_time": False,
        "buttons": [
            buttons,
            [
                get_button('⟵ к очередям', 'queuesMenu', Color.BLUE),
            ],
            [
                get_button('⟵ главное меню', 'backToDefaultKeyboard', Color.BLUE),
            ]
        ]
    }, ensure_ascii=False)


def get_materials_actions_buttons(values):
    items = values.vkApi.docs.search(q='>', search_own=1, count=200)['items']
    values.materials = items
    materials_list = []
    for doc in items:
        if doc['owner_id'] == -168330527 or doc['owner_id'] == -168366525:
            materials_list.append(doc['title'])
    if len(materials_list) == 0:
        return None

    subjects_list = []
    for material in materials_list:
        subject = ' '.join(material.split()[1:-1]).lower()
        if subject not in subjects_list and material.split()[0] == '>':
            subjects_list.append(subject)

    buttons_list = [[get_button(subject, 'showMaterialsList', Color.WHITE)] for subject in subjects_list]
    buttons_list.append([get_button('⟵ главное меню', 'backToDefaultKeyboard', Color.BLUE)])
    return json.dumps({
        "one_time": False,
        "buttons": buttons_list
    }, ensure_ascii=False)


def get_materials_list_buttons(subject, values, page_num=None):
    items = values.vkApi.docs.search(q='>', search_own=1, count=200)['items']
    pages_dict = None
    materials_list = []
    for doc in items:
        if (doc['owner_id'] == -168330527 or doc['owner_id'] == -168366525) and \
                (doc['title'].split()[1].lower() == subject):
            materials_list.append(doc['title'].lower())
    materials_list.sort()

    if len(materials_list) > 8:
        pages_dict = {0: []}
        p_num = 0
        for material in materials_list:
            if len(pages_dict[p_num]) == 6:
                p_num += 1
                pages_dict.setdefault(p_num, [])
            pages_dict[p_num].append(material)

        materials_list = pages_dict[page_num if page_num is not None else 0]

    buttons_list = [[get_button(material.split()[2], 'getFile ' + material, Color.WHITE)]
                    for material in materials_list]

    if pages_dict is not None:
        if page_num is None or page_num == 0:
            buttons_list.append([get_button('→', 'nextMaterialsPage ' +
                                            subject + ' 1', Color.GREEN)])
            if len(pages_dict) > 2:
                buttons_list.append([get_button('Конец', 'nextMaterialsPage ' + subject + ' ' +
                                                str(len(pages_dict) - 1), Color.GREEN)])

        elif (page_num + 1) == len(pages_dict):
            buttons_list.append([get_button('←', 'nextMaterialsPage ' + subject +
                                            ' ' + str(page_num - 1), Color.GREEN)])
            if len(pages_dict) > 2:
                buttons_list.append([get_button('Начало', 'nextMaterialsPage ' + subject + ' 0', Color.GREEN)])

        else:
            buttons_list.append([get_button('←', 'nextMaterialsPage ' + subject +
                                            ' ' + str(page_num - 1), Color.GREEN),
                                 get_button('→', 'nextMaterialsPage ' + subject +
                                            ' ' + str(page_num + 1), Color.GREEN)])
            if len(pages_dict) > 2:
                buttons_list.append([get_button('Начало', 'nextMaterialsPage ' + subject + ' 0', Color.GREEN),
                                     get_button('Конец', 'nextMaterialsPage ' + subject + ' ' +
                                                str(len(pages_dict) - 1), Color.GREEN)])

    buttons_list.append([get_button('⟵ все предметы', 'materialsMenu', Color.BLUE)])
    buttons_list.append([get_button('⟵ главное меню', 'backToDefaultKeyboard', Color.BLUE)])
    return json.dumps({
        "one_time": False,
        "buttons": buttons_list
    }, ensure_ascii=False)


def get_dates_for_queue_creation_buttons():
    week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
    date = datetime.now()
    weekday = datetime.weekday(date)
    days_list = []

    for i in range(5):
        if weekday == 6:  # Пропуск воскресенья
            date += timedelta(1)
            weekday = 0
        day_str = str(date.timetuple()[2])
        month = date.timetuple()[1]
        month_str = str(month)
        if (month - 10) < 0:
            month_str = '0' + month_str

        days_list.append(day_str + '.' + month_str + ' (' + week[weekday] + ')')
        date += timedelta(1)
        weekday += 1

    buttons_list = [[get_button(day, 'queueByDate', Color.BLUE)] for day in days_list]
    buttons_list.append([get_button('⟵ главное меню', 'backToDefaultKeyboard', Color.RED)])

    return json.dumps({
        "one_time": False,
        "buttons": buttons_list
    }, ensure_ascii=False)


def get_groups_for_queue_creation_buttons(date):
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                get_button('5621', 'queueByGroup ' + date, Color.BLUE),
                get_button('5622', 'queueByGroup ' + date, Color.BLUE),
                get_button('5623', 'queueByGroup ' + date, Color.BLUE)
            ],
            [
                get_button('5621 5622', 'queueByGroup ' + date, Color.BLUE),
                get_button('5621 5623', 'queueByGroup ' + date, Color.BLUE),
                get_button('5622 5623', 'queueByGroup ' + date, Color.BLUE)
            ],
            [
                get_button('5621 5622 5623', 'queueByGroup ' + date, Color.BLUE)
            ],
            [
                get_button('⟵ к выбору даты', 'createQueue', Color.RED),
                get_button('⟵ главное меню', 'backToDefaultKeyboard', Color.RED)
            ]
        ]
    }, ensure_ascii=False)


def get_subjects_for_queue_creation_buttons(values, tail_of_queue_name):
    buttons_list = []
    two_buttons_pack = []
    for sub in getSubjects(values.connect):
        two_buttons_pack.append(sub)
        if len(two_buttons_pack) == 2:
            buttons_list.append(two_buttons_pack)
            two_buttons_pack = []
    if len(two_buttons_pack) != 0:
        buttons_list.append(two_buttons_pack)

    buttons_list = [[get_button(sub, 'queueCreation ' + tail_of_queue_name, Color.BLUE)
                     for sub in two_buttons_pack] for two_buttons_pack in buttons_list]
    buttons_list.append([
        get_button('⟵ к выбору групп', 'queueByDate', Color.RED),
        get_button('⟵ главное меню', 'backToDefaultKeyboard', Color.RED)
    ])

    return json.dumps({
        "one_time": False,
        "buttons": buttons_list
    }, ensure_ascii=False)


def get_groups_for_message_buttons():
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                get_button('5621', 'infoByGroup', Color.BLUE),
                get_button('5622', 'infoByGroup', Color.BLUE),
                get_button('5623', 'infoByGroup', Color.BLUE)
            ],
            [
                get_button('5621 5622', 'infoByGroup', Color.BLUE),
                get_button('5621 5623', 'infoByGroup', Color.BLUE),
                get_button('5622 5623', 'infoByGroup', Color.BLUE)
            ],
            [
                get_button('5621 5622 5623', 'infoByGroup', Color.BLUE)
            ],
            [
                get_button('⟵ Отмена', 'backToDefaultKeyboard', Color.RED)
            ]
        ]
    }, ensure_ascii=False)


def get_asking_if_send_message_buttons():
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                get_button('Разослать', 'infoSendMessage', Color.GREEN)
            ],
            [
                get_button('⟵ Отмена', 'backToDefaultKeyboard', Color.RED)
            ]
        ]
    }, ensure_ascii=False)


def get_message_cancel_button():
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                get_button('⟵ Отмена', 'backToDefaultKeyboard', Color.RED)
            ]
        ]
    }, ensure_ascii=False)


def get_timetable_menu_buttons(values):
    group = values.users[values.item['from_id']]['group']

    if values.item['from_id'] not in getSubscribedUsers(values.connect):
        subscription_button = [get_button('Подписаться на рассылку', 'timetableSending sub', Color.GREEN)]
    else:
        subscription_button = [get_button('Отписаться от рассылки', 'timetableSending unsub', Color.RED)]

    days_dict = {'Понедельник': 'пн',
                 'Вторник': 'вт',
                 'Среда': 'ср',
                 'Четверг': 'чт',
                 'Пятница': 'пт',
                 'Суббота': 'сб',
                 'Воскресенье': 'вс'}
    days_list = []
    for day in days_dict:
        if day in getDaysForGroup(values.timetableDict, group):
            days_list.append(day)

    buttons_list = []
    three_buttons_pack = []
    for day in days_list:
        three_buttons_pack.append(day)
        if len(three_buttons_pack) == 3:
            buttons_list.append(three_buttons_pack)
            three_buttons_pack = []
    if len(three_buttons_pack) != 0:
        buttons_list.append(three_buttons_pack)

    list_of_buttons = [[get_button('Сегодня', 'oneDayTimetable', Color.WHITE),
                        get_button('Завтра', 'oneDayTimetable', Color.WHITE)]]

    for days_list in buttons_list:
        list_of_buttons.append([get_button(days_dict[day], 'oneDayTimetable ' + day, Color.BLUE)
                                for day in days_list])

    list_of_buttons.append([get_button('На всю неделю', 'askTheWeek', Color.WHITE)])
    list_of_buttons.append(subscription_button)
    list_of_buttons.append([get_button('⟵ главное меню', 'backToDefaultKeyboard', Color.BLUE)])

    return json.dumps({
        "one_time": False,
        "buttons": list_of_buttons
    }, ensure_ascii=False)


def get_asking_week_buttons():
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                get_button('Текущая', 'fullWeekTimetable', Color.WHITE)
            ],
            [
                get_button('Следующая', 'fullWeekTimetable', Color.WHITE)
            ],
            [
                get_button('Полное расписание', 'fullWeekTimetable', Color.WHITE)
            ],
            [
                get_button('⟵ в меню расписания', 'showTimetableButtons', Color.BLUE)
            ],
            [
                get_button('⟵ в главное меню', 'backToDefaultKeyboard', Color.BLUE)
            ]
        ]
    }, ensure_ascii=False)
