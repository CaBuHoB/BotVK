import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials


def getGoogleAccess():
    keys = {"access_token": None, "client_id": "108396352402276263785", "client_secret": None, "refresh_token": None,
            "token_expiry": None, "token_uri": "https://accounts.google.com/o/oauth2/token", "user_agent": None,
            "revoke_uri": "https://oauth2.googleapis.com/revoke", "id_token": None, "id_token_jwt": None,
            "token_response": None, "scopes": [], "token_info_uri": None, "invalid": False, "assertion_type": None,
            "_service_account_email": "bot56-333@bot56-209721.iam.gserviceaccount.com",
            "_scopes": "https://spreadsheets.google.com/feeds https://www.googleapis.com/auth/drive",
            "_private_key_id": os.environ['GOOGLE_PRIVATE_KEY_ID'], "_user_agent": None, "_kwargs": {},
            "_private_key_pkcs8_pem": os.environ['GOOGLE_PRIVATE_KEY'].replace('\\n', '\n'),
            "_class": "ServiceAccountCredentials", "_module": "oauth2client.service_account"}
    credentials = ServiceAccountCredentials.from_json(keys)
    return gspread.authorize(credentials)


def getNamesListFromGoogle(group):
    account = getGoogleAccess()
    file = account.open("Tables")
    worksheet = file.worksheet(group)
    names_list = worksheet.col_values(1)  # Names
    mark_list = worksheet.col_values(2)  # Marks (already registrated or not)

    listForButtons = []
    for name in names_list:
        if mark_list[names_list.index(name)] != 'Registrated':
            listForButtons.append(name)

    return listForButtons


def getGroupNumbersFromGoogle():
    account = getGoogleAccess()
    file = account.open("Tables")
    sheets_list = file.worksheets()

    listForButtons = []
    for sheetName in sheets_list:
        listForButtons.append(sheetName.title)

    return listForButtons


def setNameSelectedToGoogle(name, group):
    account = getGoogleAccess()
    sheets = account.open("Tables")
    worksheet = sheets.worksheet(group)

    cell = worksheet.find(name)
    worksheet.update_cell(cell.row, cell.col + 1, 'Registrated')


def setNameUnSelectedToGoogle(name, group):
    account = getGoogleAccess()
    sheets = account.open("Tables")
    worksheet = sheets.worksheet(group)

    cell = worksheet.find(name)
    worksheet.update_cell(cell.row, cell.col + 1, '0')


def getTimetableFromGoogle():
    timetableDict = {}

    account = getGoogleAccess()
    file = account.open("Timetable")

    for group in range(5621, 5624):
        worksheet = file.worksheet(str(group))
        daysOfWeek = worksheet.row_values(1)
        timetableForGroup = {}

        for nameOfDay in daysOfWeek:
            timetableForGroup[nameOfDay] = {}
            lessons_list = worksheet.col_values(worksheet.find(nameOfDay).col)[1:]

            for lesson in lessons_list:
                timename, isUpper, typeSubject, name, hall, teacher, groups = lesson.split('\n')

                groups = groups.split()
                if isUpper == 'true':
                    isUpper = True
                elif isUpper == 'false':
                    isUpper = False
                else:
                    isUpper = None

                if timename not in timetableForGroup[nameOfDay]:
                    timetableForGroup[nameOfDay][timename] = []

                timetableForGroup[nameOfDay][timename].append({
                    "isUpper": isUpper,
                    "type": typeSubject,
                    "name": name,
                    "lecture hall": hall,
                    "teacher": teacher,
                    "group": groups
                })

        timetableDict[str(group)] = timetableForGroup

    return timetableDict

l = getNamesListFromGoogle('5622')
a = 0
b = 1