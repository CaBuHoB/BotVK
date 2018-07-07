# -*- coding: utf-8 -*-

# здесь должны быть функции для работы с бд
from Bot.Basis.DataBase.DBWorker import getConnect


def getAllUsers():
    connect = getConnect()
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM users')

    users = []
    for fetchone in cursor:
        users.append({
            'id': fetchone[0],
            'name': fetchone[1],
            'surname': fetchone[2],
            'group': fetchone[3]
        })
    cursor.close()
    connect.close()

    return users


users = getAllUsers()
print(users)
for user in users:
    if 'Maxim' == user['name']:
        print(user)
