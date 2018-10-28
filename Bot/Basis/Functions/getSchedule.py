from Bot.Basis.YandexGoogle.GoogleTables import getTimetableFromGoogle


def getTimetableDict():
    return getTimetableFromGoogle()


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
