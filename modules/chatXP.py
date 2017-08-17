from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import tokenKeys
from random import randrange
from time import time

import psycopg2 as postG
import discord

host = tokenKeys.dbHost
user = tokenKeys.dbUser
passW = tokenKeys.dbPass

class timeCheck:
    def __init__(self):
        self.lastTime = time()
        self.messageSent = {}

    def resetTime(self):
        print('It\'s been over a minute. Time to reset point timer')
        self.lastTime = time()
        self.messageSent = {}

    def getMessage(self):
        return self.messageSent

getTime = timeCheck()

def canGetXP(message):
    if time() - getTime.lastTime > 59:
        getTime.resetTime()

    messageSent = getTime.getMessage()

    try:
        if messageSent[message.server.id][message.author.id]:
            pass
    except:
        try:
            messageSent[message.server.id][message.author.id] = True
            print('This is possible')
        except:
            messageSent[message.server.id] = {}
            messageSent[message.server.id][message.author.id] = True
        addXP(message)

def addXP(message):
    server = message.server.id
    test = 'server_{}'.format(server)
    conn_string = 'host = {} dbname = {} user = {} password = {}'.format(host, test, user, passW)
    conn = postG.connect(conn_string)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute('SELECT level, xp, totalXP FROM users WHERE ID = %s', (message.author.id,))
    result = cursor.fetchone()
    level = result[0]
    xp = result[1]
    tXP = result[2]

    gain = randrange(30)
    xp += gain
    tXP += gain
    print('{} has gained {} points!'.format(message.author.name, gain))
    if xp >= (level*150):
        xp -= (level*150)
        level += 1
        print('{} has leveled up to level {}!'.format(message.author.name, level))

    cursor.execute('UPDATE users SET level = %s, xp = %s, totalXP = %s WHERE id = %s', (level, xp, tXP, message.author.id))
    cursor.close()
    conn.close()


async def checkXP( message, client):
    if message.author.id != client.user.id:
        msg = message.content.split()

        if msg[0] == '!points':
            server = message.server.id
            test = 'server_{}'.format(server)
            conn_string = 'host = {} dbname = {} user = {} password = {}'.format(host, test, user, passW)
            conn = postG.connect(conn_string)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            cursor.execute('SELECT xp, totalXP FROM users WHERE ID = %s', (message.author.id,))
            result = cursor.fetchone()
            currXP = result[0]
            totalXP = result[1]

            xpEmbed = discord.Embed(title='', description='', colour=0x0055FF)
            xpEmbed.add_field(name='Current Points:', value=currXP, inline=True)
            xpEmbed.add_field(name='Total Points:', value=totalXP, inline=True)
            xpEmbed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
            await client.send_message(message.channel, embed=xpEmbed)