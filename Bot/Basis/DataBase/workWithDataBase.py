# -*- coding: utf-8 -*-

import psycopg2


def getConnect():
    dbname = 'd83jm6venn88s5'
    user = 'uniyqmorkhqebp'
    password = '49fc88f50aa5ab5769aef22fbc2313bb56f8b14ed38e3dc08b5157f5c35c9d9e'
    host = 'ec2-54-217-250-0.eu-west-1.compute.amazonaws.com'
    port = 5432

    con = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    return con


def getAllUsers(connect):
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM users')

    users = {}
    for userData in cursor:
        users.setdefault(
            userData[0],
            {
                'name': userData[1],
                'surname': userData[2],
                'group': userData[3]
            }
        )
    cursor.close()

    return users


def addPersonToDB(connect, id, name, surname, group):
    cursor = connect.cursor()

    cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s)', [id, name, surname, group])
    cursor.close()
    connect.commit()


def createQueueInBD(connect, name):
    cursor = connect.cursor()

    cursor.execute('CREATE TABLE queue.{} (id int NOT NULL, name varchar(50) NOT NULL);'.format(name))
    cursor.close()
    connect.commit()


def removeQueueInBD(connect, queue):
    cursor = connect.cursor()

    cursor.execute('DROP TABLE queue.{}'.format(queue))
    cursor.close()
    connect.commit()


def removeFromDateDeleted(connect, queue):
    cursor = connect.cursor()

    cursor.execute('DELETE FROM public."date deleted tables" WHERE name = %s', [queue])
    cursor.close()
    connect.commit()


def getDateDeletedTables(connect):
    cursor = connect.cursor()

    cursor.execute('SELECT * FROM public."date deleted tables"')
    nameDate = [[table[0], table[1], table[2]] for table in cursor]
    cursor.close()

    return nameDate


def addTableInDateDeleteTable(connect, name, date, id):
    cursor = connect.cursor()

    cursor.execute('INSERT INTO public."date deleted tables" VALUES (%s, %s, %s)', [name, date, id])
    cursor.close()
    connect.commit()


def updateDateInDateDeleted(connect, queue, newDate):
    cursor = connect.cursor()

    cursor.execute('UPDATE public."date deleted tables" SET date = %s WHERE name = %s', [newDate, queue])
    cursor.close()
    connect.commit()


def getQueueNames(connect):
    cursor = connect.cursor()

    cursor.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = %s', ['queue'])
    tables = [answ[0] for answ in cursor]
    cursor.close()

    return tables


def getQueueList(connect, queue):
    cursor = connect.cursor()

    cursor.execute('SELECT name FROM queue.{}'.format(queue))
    queueList = [name[0] for name in cursor]
    cursor.close()

    return queueList


def getSubjects(connect):
    cursor = connect.cursor()

    cursor.execute('SELECT name FROM public.subjects')
    subjectsList = [name[0] for name in cursor]
    cursor.close()

    return subjectsList


def removeFromQueueInDB(connect, queue, id):
    cursor = connect.cursor()

    cursor.execute('DELETE FROM queue.{} WHERE id = {}'.format(queue, id))
    cursor.close()
    connect.commit()


def setToQueue(connect, queue, id, name):
    cursor = connect.cursor()

    cursor.execute('SELECT * FROM queue.{} WHERE id = {}'.format(queue, id))
    if len(cursor.fetchall()) != 0:
        cursor.execute('DELETE FROM queue.{} WHERE id = {}'.format(queue, id))
        connect.commit()
        cursor.execute('INSERT INTO queue.{} VALUES (%s, %s)'.format(queue), [id, name])
    else:
        cursor.execute('INSERT INTO queue.{} VALUES (%s, %s)'.format(queue), [id, name])

    cursor.close()
    connect.commit()

    return True


def subscribePerson(connect, user_id):
    cursor = connect.cursor()

    cursor.execute('INSERT INTO public.subscribers VALUES (%s)', [user_id])
    cursor.close()
    connect.commit()


def unSubscribePerson(connect, user_id):
    cursor = connect.cursor()

    cursor.execute('DELETE FROM public.subscribers WHERE id = {}'.format(user_id))
    cursor.close()
    connect.commit()


def getSubscribedUsers(connect):
    cursor = connect.cursor()

    cursor.execute('SELECT id FROM public.subscribers')
    subscribers = [id[0] for id in cursor]
    cursor.close()

    return subscribers
