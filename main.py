import _thread
import asyncio
import json
from time import time, sleep
import discord
from commands import chatBot, globalCommands, modCommands, promotions, ytStream, pointCommands
from config import tokenKeys
from modules import autoMod, youtubeChecker
from modules import database
from modules.dataClasses import Server
from modules.chatXP import canGetXP, checkXP
from datetime import datetime

try:
    database.connectToDB()
    dbConnect = True
except:
    dbConnect = False

if dbConnect:
    client = discord.Client()
else:
    print('Unable to connect to database')
    print('Bot requires a database connection')

serverDict = {}


@client.event
async def on_ready():
    servers = len(client.servers)
    users = len(set(client.get_all_members()))

    print('Any new servers since we were online?')
    for server in client.servers:
        try:
            #database.updateDB(server)
            pass
        except:
            pass
        try:
            database.addServer(server)
        except:
            pass
        serverDict[server.id] = Server(server)

    print('---------------------')
    print('| Started MidgetBot |')
    print('---------------------')
    print('| Serving: {} Users'.format(users))
    print('| In: {} Servers'.format(servers))
    print('| BotID: {}'.format(client.user.id))
    print('---------------------')

    _thread.start_new_thread(constCheck, (client,))

@client.event
async def on_message(message):

    msg = message.content.split()
    print('| {} | {} | {} | {} | {} | {} | {} | {}'.format(
                                                       datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
                                                       message.server.name,
                                                       message.server.id,
                                                       message.channel.name,
                                                       message.channel.id,
                                                       message.author.name,
                                                       message.author.id,
                                                       message.content))

    if len(message.attachments) >= 1:
        await client.add_reaction(message, '👍')
        await client.add_reaction(message, '👎')

    else:
        # Make sure it's not the bot sending the message
        if message.author.id != client.user.id:
            await modCommands.checkCommand(message, client)
            if autoMod.doChecks(message):
                await client.delete_message(message)
            else:
                if message.author.id == '95677195162222592' and msg[0] == '!debug':
                    for chan in message.server.channels:
                        print(chan)
                await process_command(message, client)
                canGetXP(message)


@client.event
async def on_message_edit(oldM, newM):
    print('Message edited!')
    if newM.author.id != client.user.id:
        autoMod.doChecks(newM)
        print('-------------------------------------')
        print('| {} / {} edited a message and it was deleted'.format(newM.author.name, newM.author.id))
        print('| Old message: {} '.format(oldM.content))
        print('| New message: {} '.format(newM.content))
        print('-------------------------------------')
        await client.delete_message(newM)

@client.event
async def on_member_join(member):
    print('-------------------------------------')
    print('| New member has joined {}! - {} | {}'.format(member.server.name, member.name, member.id))
    print('-------------------------------------')
    database.addUser(member)

@client.event
async def on_server_join(server):
    print('-------------------------------------')
    print('| Joined a new server! - {}'.format(server.id))
    print('| Server name - {}'.format(server.name))
    print('-------------------------------------')
    database.addServer(server)


@client.event
async def on_server_remove(server):
    print('-------------------------------------')
    print('| We have be removed from this server: {}'.format(server.name))
    print('| The ID of this server is: {}'.format(server.id))
    print('-------------------------------------')
    with open('config/leftServers', 'a') as af:
        af.write(server.id)
    #ToDo:
    #     - Remove the server database when the bot leaves a server

@client.event
async def on_member_remove(member):
    print('-------------------------------------')
    print('| User: {} has left server: {}'.format(member.name, member.server.name))
    print('| The ID this user is: {} and the server: {}'.format(member.id, member.server.id))
    print('-------------------------------------')
    with open ('config/leftMembers', 'a') as af:
        af.write('{} | {}'.format(member.id, member.server.id))

# This is where all the commands are processed
# This will be updated when the bot becomes more customisable between server
async def process_command(message, client):
    try:
        print(message.embeds[0])
    except IndexError:
        await chatBot.chatBotTalk(message, client)
        await ytStream.checkCommand(message, client)
        await chatBot.checkCommand(message, client)
        await promotions.checkCommand(message, client)
        await globalCommands.checkCommand(message, client)
        await checkXP(message, client)
        await pointCommands.quoteSystem(message, client)


# This is a huge mess
# Will clean up in a future update
def constCheck(clienter):
    with open('config/doneAnnounce') as announced:
        content = announced.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    prevLive = [x.strip('\n') for x in content]
    while(True):
        currLive = []
        sleep(60)
        with open('config/onCooldown') as jsonLoad:
            cdJson = json.load(jsonLoad)
        with open('config/serverStreamConfig') as jsonLoad:
            configJson = json.load(jsonLoad)
        cdList = []
        for dChansK, dChansV in cdJson.items():
            for yChansK, yChansV in dChansV.items():
                if time() - ((configJson[dChansK]['cooldown']*60)+yChansV) > 0:
                    cdList.append(yChansK)
        chanList = youtubeChecker.findLiveChans(cdList)
        if chanList != []:
            for x in chanList:
                ytG=''
                if configJson[x[0]]['ytGaming']:
                    ytG = 'gaming.'
                iThmb = configJson[x[0]]['imgThumb']
                mention = ''
                if configJson[x[0]]['mention'] != 'none':
                    mention = '@' + configJson[x[0]]['mention'] + ' | '

                currLive.append(x[0] + ' - ' + x[1][2])
                if (x[0] + ' - ' + x[1][2]) in prevLive:
                    pass
                else:
                    prevLive.append(x[0] + ' - ' + x[1][2])
                    try:
                        # Tuple setup: (channelID, (chanID, title, liveLink, chanName, setThumb))
                        if x[1][4] and iThmb:
                            coro = clienter.send_file(discord.Object(id=x[0]), 'thumbnails/'+x[1][0]+'temp.jpg',
                                                         content=(
                                                         mention + x[1][3] + ' is now streaming: \"__***' +
                                                          x[1][1] + '***__\" at: https://'+ytG+'youtube.com/watch?v=' + x[1][2]))
                        else:
                            coro = clienter.send_message(discord.Object(id=x[0]),
                                                          mention + x[1][3] + ' is now streaming: \"__***' +
                                                          x[1][1] + '***__\" at: https://'+ytG+'youtube.com/watch?v=' + x[1][2])
                        fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
                    except:
                        print('shit')
                    try:
                        fut.result()
                        cdJson[x[0]][x[1][0]] = time()
                    except:
                        print("There was an issue with the thread")
            newPrevLive = []
            for vid in prevLive:
                if vid in currLive and vid not in newPrevLive:
                    newPrevLive.append(vid)
                else:
                    pass
            prevLive = newPrevLive
            open('config/doneAnnounce', 'w').close()
            with open('config/doneAnnounce', 'w') as announced:
                for item in prevLive:
                    announced.write("%s\n" % item)
            with open('config/onCooldown', 'w') as jsonWrite:
                json.dump(cdJson, jsonWrite)
    return 1

client.run(tokenKeys.discord)
