import psycopg2 as postG
from config import tokenKeys
from datetime import datetime
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

host = tokenKeys.dbHost
user = tokenKeys.dbUser
passW = tokenKeys.dbPass

def connectToDB():
    dbName = 'MAIN'

    conn_string = 'host = {} dbname = {} user = {} password = {}'.format(host, dbName, user, passW)
    conn = postG.connect(conn_string)
    conn.cursor()
    print('Connection successful')


def updateDB(server):
    test = 'server_{}'.format(server.id)
    conn_string = 'host = {} dbname = {} user = {} password = {}'.format(host, test, user, passW)
    conn = postG.connect(conn_string)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute('ALTER TABLE roleperms ADD addquote BOOLEAN DEFAULT TRUE')
    cursor.execute('ALTER TABLE roleperms ADD editquote BOOLEAN DEFAULT FALSE')
    cursor.execute('ALTER TABLE roleperms ADD delquote BOOLEAN DEFAULT FALSE')
    cursor.close()
    conn.close()


def addServer(server):
    dbName = 'MAIN'

    conn_string = 'host = {} dbname = {} user = {} password = {}'.format(host, dbName, user, passW)
    conn = postG.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO serverlist VALUES(%s, %s, %s, %s)", (server.id, server.name, len(server.members), datetime.today()))
    cursor.execute('INSERT INTO settings VALUES (%s, 250)', (server.id,))
    print('Oh look a new server: {}'.format(server.name))
    print('Or in a way that we can find the server: {}'.format(server.id))

    cursor.close()
    conn.commit()
    conn.close()
    setupServerDB(server)


def setupServerDB(server):
    conn_string = 'host = {} dbname=postgres user = {} password = {}'.format(host, user, passW)
    conn = postG.connect(conn_string)
    cursor = conn.cursor()

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    test = 'server_{}'.format(server.id)
    print(test)
    cursor.execute('CREATE DATABASE {}'.format(test))
    cursor.close()
    conn.commit()
    conn.close()

    conn_string = 'host = {} dbname = {} user = {} password = {}'.format(host, test, user, passW)
    conn = postG.connect(conn_string)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    print('Make settings')
    cursor.execute('CREATE TABLE settings (chanID BIGINT PRIMARY KEY, '
                                          'canPromoteYT BOOLEAN DEFAULT TRUE, '
                                          'canPromoteDiscord BOOLEAN DEFAULT TRUE, '
                                          'canChatBot BOOLEAN DEFAULT TRUE,'
                                          'checkRank BOOLEAN DEFAULT TRUE,'
                                          'earnXP BOOLEAN DEFAULT TRUE,'
                                          'slowMode BOOLEAN DEFAULT FALSE,'
                                          'slowTime INT DEFAULT 0,'
                                          'quoteAddCost INT DEFAULT 500)')
    for chan in server.channels:
        cursor.execute('INSERT INTO settings (CHANID) VALUES (%s)', (chan.id,))
    cursor.execute('INSERT INTO settings (CHANID) VALUES (0)')

    print('Make users')
    cursor.execute('CREATE TABLE users (id BIGINT PRIMARY KEY,'
                                       'name TEXT,'
                                       'messagesSent INT DEFAULT 0,'
                                       'level INT DEFAULT 1,'
                                       'xp INT DEFAULT 0,'
                                       'totalXP INT DEFAULT 0,'
                                       'joined TIMESTAMPTZ)')
    for dUser in server.members:
        cursor.execute('INSERT INTO users (ID, NAME) VALUES (%s, %s)', (dUser.id, dUser.name))


    print('Make roleperms')
    cursor.execute('CREATE TABLE roleperms (id SERIAL PRIMARY KEY,'
                   'name TEXT,'
                   'slow BOOLEAN DEFAULT FALSE,'
                   'mute BOOLEAN DEFAULT FALSE,'
                   'banword BOOLEAN DEFAULT FALSE,'
                   'timeout BOOLEAN DEFAULT FALSE,'
                   'clear BOOLEAN DEFAULT FALSE,'
                   'addquote BOOLEAN DEFAULT TRUE,'
                   'editquote BOOLEAN DEFAULT FALSE,'
                   'delquote BOOLEAN DEFAULT FALSE)')
    for role in server.role_hierarchy:
        cursor.execute('INSERT INTO roleperms (NAME) VALUES (%s)', (str(role),))

    print('make bannedWords')
    cursor.execute('CREATE TABLE bannedWords (id SERIAL PRIMARY KEY,'
                   'word TEXT,'
                   'hard BOOLEAN DEFAULT FALSE)')

    print('make quotes')
    cursor.execute('CREATE TABLE quotes (ID SERIAL PRIMARY KEY,'
                   'name TEXT,'
                   'quote TEXT,'
                   'date TIMESTAMPTZ,'
                   'creator TEXT)')

def addUser(member):
    test = 'server_{}'.format(member.server.id)
    conn_string = 'host = {} dbname = {} user = {} password = {}'.format(host, test, user, passW)
    conn = postG.connect(conn_string)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (ID, NAME, joined) VALUES (%s, %s)', (member.id, member.name, datetime.today()))
    cursor.close()
    conn.close()
