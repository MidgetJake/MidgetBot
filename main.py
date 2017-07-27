import _thread
import asyncio
import json
import time

import discord

from commands import chatBot, globalCommands, modCommands, promotions, ytStream
from config import tokenKeys
from modules import autoMod, youtubeChecker

client = discord.Client()

@client.event
async def on_ready():
    print('Starting the bot:')
    print(client.user.name)
    print(client.user.id)
    print('----------------')
    #client.loop.create_task(constCheck())
    _thread.start_new_thread(constCheck, (client,))
    #startChecker()

@client.event
async def on_message(message):

    msg = message.content.split()
    print(message.server.name + ' | ' + message.channel.name + ' | ' + message.channel.id + ' | ' + message.author.name + " | " + message.content + " | " + message.author.id)

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
                await chatBot.chatBotTalk(message, client)
                await ytStream.checkCommand(message, client)
                await chatBot.checkCommand(message, client)
                await promotions.checkCommand(message, client)
                await globalCommands.checkCommand(message, client)






def constCheck(clienter):
    with open('config/doneAnnounce') as announced:
        content = announced.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    prevLive = [x.strip('\n') for x in content]
    #prevLive = []
    while(True):
        currLive = []
        time.sleep(60)
        with open('config/onCooldown') as jsonLoad:
            cdJson = json.load(jsonLoad)
        with open('config/serverStreamConfig') as jsonLoad:
            configJson = json.load(jsonLoad)
        cdList = []
        for dChansK, dChansV in cdJson.items():
            for yChansK, yChansV in dChansV.items():
                if time.time() - ((configJson[dChansK]['cooldown']*60)+yChansV) > 0:
                    cdList.append(yChansK)
        chanList = youtubeChecker.findLiveChans(cdList)
        if chanList != []:
            for x in chanList:
                ytG=''
                if configJson[x[0]]['ytGaming']:
                    ytG = 'gaming.'
                iThmb = configJson[x[0]]['imgThumb']
                mention=''
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
                        cdJson[x[0]][x[1][0]] = time.time()
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
