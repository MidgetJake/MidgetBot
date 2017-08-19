from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime
from random import randrange
from config import tokenKeys
import psycopg2 as postG
import Eball

host = tokenKeys.dbHost
user = tokenKeys.dbUser
passW = tokenKeys.dbPass

async def checkCommand(message, client):

    msg = message.content.split()
    # The wisdom of 8ball is great!
    if msg[0].lower() == '!8ball':
        await client.send_message(message.channel, Eball.eBall(randrange(20)))

    if msg[0].lower() in ['!suggestion', '!s', '!suggest']:
        conn_string = 'host = {} dbname = {} user = {} password = {}'.format(host, 'MAIN', user, passW)
        conn = postG.connect(conn_string)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO suggestions (idea, suggestor, date) '
                       'VALUES (%s, %s, %s)', (' '.join(msg[1::]), message.author.name, datetime.today()))
        cursor.close()
        conn.close()
        await client.send_message(message.channel, 'Thanks for your suggestion!')

    if msg[0].lower() in ['!joined', 'sj']:
        if len(message.mentions) == 1:
            for user in message.mentions:
                await client.send_message(message.channel, 'User joined this server at: {}'.format(user.joined_at.strftime('%d-%m-%Y %H:%M:%S')))

    # Returns a random number up to the range specified by user
    #if msg[0] == '!rand':
    #    try:
    #        r = int(float(msg[1]))
    #        await client.send_message(message.channel, randrange(r))
    #    except ValueError:
    #        await client.send_message(message.channel, 'The second argument must be a number')
    #    except IndexError:
    #        await client.send_message(message.channel, 'A number is required')