# -*- coding: utf-8 -*-


def getAllUsers(connect):
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

    return users

# TODO здесь нужно созддать все методы для работы с БД
