import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials


def getGoogleAccess():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    dir = os.path.split(os.path.abspath(__file__))[0]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(dir + '/keys.json', scope)
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
