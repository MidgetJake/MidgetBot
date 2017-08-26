#########################################
# This is for commands that cost points #
#########################################
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from modules.helpers import checkRole
from config import tokenKeys
from datetime import datetime
import psycopg2 as postG
import discord


host = tokenKeys.dbHost
user = tokenKeys.dbUser
passW = tokenKeys.dbPass

async def quoteSystem(message, client):
    msg = message.content.split()
    if msg[0] == '!quote' or msg[0] == '!q':
        if msg[1] == 'add':
            if checkRole(message, client, 'addquote') or message.author.permissions_in(message.channel).administrator:
                cost = getCommandCost(message, 'quoteAddCost')
                print(cost)
                if checkPoints(message, cost):
                    server = message.server.id
                    test = 'server_{}'.format(server)
                    conn_string = 'host = {} dbname = {} user = {} password = {}'.format(host, test, user, passW)
                    conn = postG.connect(conn_string)
                    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO quotes (name, quote, date, creator) VALUES (%s, %s, %s, %s)',
                                   (msg[2], ' '.join(msg[3::]), datetime.today(), message.author.id))

                    cursor.execute('SELECT * FROM quotes')
                    count = len(cursor.fetchall())
                    cursor.close()
                    conn.close()

                    quote = '\"{}\" - {} {}'.format(' '.join(msg[3::]), msg[2], datetime.today().strftime('%d-%m-%Y'))

                    embed = discord.Embed(title='', description='', colour=0x0055FF)
                    embed.add_field(name='Quote #{}'.format(count), value=quote, inline=True)
                    embed.set_footer(text='Quoted by: {}'.format(message.author.name))
                    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    await client.send_message(message.channel, embed=embed)
                    print('| Quote Added')
                else:
                    await client.send_message(message.channel, 'You do not have enough points to add a quote. It requires {} points'.format(cost))
        elif msg[1] in ['remove', 'delete', 'rem', 'del']:
            if checkRole(message, client, 'delquote') or message.author.permissions_in(message.channel).administrator:
                try:
                    qNum = int(msg[2])
                    server = message.server.id
                    test = 'server_{}'.format(server)
                    conn_string = 'host = {} dbname = {} user = {} password = {}'.format(host, test, user, passW)
                    conn = postG.connect(conn_string)
                    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                    cursor = conn.cursor()
                    cursor.execute('SELECT MAX(id) FROM quotes')
                    result = cursor.fetchone()
                    print(result)
                    if qNum > result[0]:
                        await client.send_message(message.channel, 'Quote #{} doesn\' exist!'.format(qNum))
                    else:
                        cursor.execute('SELECT * FROM quotes WHERE id = %s', (qNum,))
                        delQ = cursor.fetchone()
                        buildS = ''
                        for v in delQ:
                            buildS += '{} | '.format(v)
                        buildS += '\n'
                        with open('deletedQuotes', 'a') as af:
                            af.write(buildS)
                        cursor.execute('DELETE FROM quotes WHERE id = %s', (qNum,))
                        cursor.execute('UPDATE quotes SET id = id - 1 WHERE id > %s', (qNum,))
                        maxN = result[0] - 1
                        cursor.execute('SELECT setval(\'quotes_id_seq\', %s)', (maxN,))
                        print('| Quote #{} has been deleted from: {}'.format(qNum, message.server.name))
                        await client.send_message(message.channel, 'Quote #{} has been deleted!'.format(qNum))
                except:
                    await client.send_message(message.channel, 'Use a valid number to remove a quote')
        else:
            try:
                number = int(msg[1])
                server = message.server.id
                test = 'server_{}'.format(server)
                conn_string = 'host = {} dbname = {} user = {} password = {}'.format(host, test, user, passW)
                conn = postG.connect(conn_string)
                cursor = conn.cursor()
                cursor.execute('SELECT name, quote, date, creator FROM quotes WHERE id = %s', (number,))

                result = cursor.fetchone()
                if result is not None:
                    quote = '\"{}\" - {} {}'.format(result[1], result[0], result[2].strftime('%d-%m-%Y'))

                    quoter = discord.utils.find(lambda m: m.id == result[3], message.server.members)
                    if quoter is None:
                        quoter = '<User has left server>'

                    embed = discord.Embed(title='', description='', colour=0x0055FF)
                    embed.add_field(name='Quote #{}'.format(number), value=quote, inline=True)
                    embed.set_footer(text='Quoted by: {}'.format(quoter))
                    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    await client.send_message(message.channel, embed=embed)
                else:
                    await client.send_message(message.channel, 'Quote #{} does not exist!'.format(number))

            except TypeError:
                pass



def checkPoints(message, points):
    server = message.server.id
    test = 'server_{}'.format(server)
    conn_string = 'host = {} dbname = {} user = {} password = {}'.format(host, test, user, passW)
    conn = postG.connect(conn_string)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute('SELECT xp FROM users WHERE ID = %s', (message.author.id,))
    result = cursor.fetchone()
    uPoints = result[0]

    # Mods can make quotes for free!
    if message.author.permissions_in(message.channel).administrator:
        return True

    if uPoints >= points:
        newPoints = uPoints - points
        cursor.execute('UPDATE users SET xp = %s WHERE ID = %s', (newPoints,message.author.id))
        cursor.close()
        conn.close()
        return True
    else:
        return False


def getCommandCost(message, command):
    conn_string = 'host = {} dbname = {} user = {} password = {}'.format(host, 'MAIN', user, passW)
    conn = postG.connect(conn_string)
    cursor = conn.cursor()
    sID = '{}'.format(message.server.id)
    cursor.execute('SELECT * FROM settings WHERE serverID = %s', (sID,))
    result = cursor.fetchone()
    cost = result[1]
    return cost