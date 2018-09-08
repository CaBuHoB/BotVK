import requests
import json
from bs4 import BeautifulSoup


def getUrlGroups(groupList):
    url = 'http://rasp.guap.ru'
    r = requests.get(url)

    soup = BeautifulSoup(r.text, features="lxml")
    groupDict = soup.find_all('span')[1]
    groupDict = groupDict.find_all('option')
    groupDict = {group.text: group['value'] for group in groupDict}

    urlDict = {}
    for group in groupList:
        urlDict[str(group)] = 'http://rasp.guap.ru' + '/?g=' + groupDict[str(group)]

    return urlDict


def getDate():
    url = 'http://rasp.guap.ru'
    r = requests.get(url)

    soup = BeautifulSoup(r.text, features="lxml")
    date = soup.find_all('p')[0].text.split(' ')
    dayWeek = date[2].replace(',', '')
    isUpper = bool(date[9][1])

    return {'dayWeek': dayWeek, 'isUpper': isUpper}


def getTimetableDict(groupList):
    timetableDict = {}
    url = getUrlGroups(groupList)
    for group in groupList:
        r = requests.get(url[str(group)])
        lessons = {}

        soup = BeautifulSoup(r.text, features="lxml")
        lessonList = soup.find('div', {'class': 'result'})
        dayOfWeek = lessonList.find_all('h3')
        for day in dayOfWeek:
            nameOfDay = day.text
            lessons[nameOfDay] = {}
            nextSibling = day.nextSibling
            while nextSibling is not None and nextSibling.name != 'h3':
                lessonNumber = nextSibling.text
                nextSibling = nextSibling.nextSibling

                lessonName = []
                while nextSibling is not None and nextSibling.name == 'div':
                    name = nextSibling.next.text
                    teacher = nextSibling.next.nextSibling.next.text
                    if nextSibling.next.nextSibling.next.nextSibling is not None:
                        lectureHall = nextSibling.next.nextSibling.next.nextSibling.text
                    else:
                        lectureHall = teacher
                        teacher = None

                    lessonName.append([name, teacher, lectureHall])
                    nextSibling = nextSibling.nextSibling

                lessons[nameOfDay][lessonNumber] = lessonName

        for day in lessons:
            for lessonNumber in lessons[day]:
                lectures = []
                for classUniversity in lessons[day][lessonNumber]:
                    classUniversity[0] = classUniversity[0].split(' – ')
                    if classUniversity[0][0][0] == '▲' or classUniversity[0][0][0] == '▼':
                        isUpper = True if classUniversity[0][0][0] == '▲' else False
                        classUniversity[0][0] = classUniversity[0][0][2:]
                    else:
                        isUpper = None
                    if classUniversity[1] is not None:
                        classUniversity[1] = classUniversity[1].split('-')[0].split(':')[1]
                    classUniversity[2] = classUniversity[2].split(': ')[1].split('; ')

                    lectures.append({'isUpper': isUpper,
                                     'type': str(classUniversity[0][0]).strip(),
                                     'name': str(classUniversity[0][1]).strip(),
                                     'lecture hall': str(classUniversity[0][2]).strip(),
                                     'teacher': str(classUniversity[1]).strip(),
                                     'group': classUniversity[2]})

                lessons[day][lessonNumber] = lectures

        file = str(group) + '.json'
        with open(file, 'w') as outfile:
            json.dump(lessons, outfile, ensure_ascii=False, indent=4)

        timetableDict[str(group)] = lessons

    return timetableDict


def getTimetableByDay(timetableDict, group, day, isUpper):
    timetable = timetableDict[str(group)][day]
    timetableStr_head = '📅 ' + day + '\n\n'
    timetableStr = ''
    for lesson in timetable:
        les = timetable[lesson]
        if (isUpper is not None) and (sum([0 if (l['isUpper'] != isUpper
           and l['isUpper'] is not None) else 1 for l in les]) == 0):
            continue
        timetableStr += '🔔 ' + lesson + '\n'
        for l in les:
            if l['isUpper'] == isUpper or l['isUpper'] is None or isUpper is None:
                timetableStr += '▲ ' if l['isUpper'] is True else ''
                timetableStr += '▼ ' if l['isUpper'] is False else ''
                timetableStr += l['type'] + ' - ' + l['name'] + ' '
                timetableStr += '(' + l['teacher'] + ')\n'
                timetableStr += l['lecture hall'] + ' (' + ', '.join((group for group in l['group'])) + ')\n'
        timetableStr += '\n'

    if timetableStr == '':
        return ''
    return timetableStr_head + timetableStr


def getTimetableByWeek(timetableDict, group, isUpper):
    timetableStr = ''
    for day in timetableDict[str(group)]:
        timetableStr += getTimetableByDay(timetableDict, group, day, isUpper)

    return timetableStr


def getDaysForGroup(timetableDict, group):
    timetable = timetableDict[str(group)]
    return [day for day in timetable]
