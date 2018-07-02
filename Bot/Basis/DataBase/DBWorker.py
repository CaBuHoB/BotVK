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
