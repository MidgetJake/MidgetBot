import asyncio
from random import randrange
import discord
import Eball
import botChat
import tokenKeys
import json
import youtubeChecker
import _thread
import time
import corrector

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

            if message.author.id == '95677195162222592' and msg[0] == '!debug':
                for chan in message.server.channels:
                    print(chan)

            if message.author.id == "276138499554672651" and message.content == "You suck":
                await client.send_message(message.channel, "Not as much as you... " + message.author.mention);

            #If the bot is mentioned repsond with the chatterbot
            if '<@273529250689318923>' in message.content:
                await client.send_message(message.channel, botChat.botChat(message.content))

            # Returns a random number up to the range specified by user
            if msg[0] == '!rand':
                try:
                    r = int(float(msg[1]))
                    await client.send_message(message.channel, randrange(r))
                except ValueError:
                    await client.send_message(message.channel, 'The second word must be a number')
                except IndexError:
                    await client.send_message(message.channel, 'A number is required')

            # Sah dude
            if message.content.lower().startswith('sah'):
                await client.send_message(message.channel, 'Sah dude')

            # Respond to some rude remarks
            if (msg[0].lower() == 'fuck') and (msg[1].lower() == 'you'):
                await client.send_message(message.channel, 'Fuck you too ' + message.author.mention)

            # The wisdom of 8ball is great!
            if msg[0].lower() == '8ball':
                await client.send_message(message.channel, Eball.eBall(randrange(16)))






            if message.author.id == '95677195162222592' and msg[0].lower() == '!setupyt':
                with open('onCooldown') as jsonLoad:
                    cdJson = json.load(jsonLoad)
                with open('serverYTSetup') as jsonfile:
                    jsonTmp = json.load(jsonfile)
                try:
                    jsonTmp[message.channel.id].append(msg[1])
                    try:
                        cdJson[message.channel.id][msg[1]] = 0
                    except:
                        cdJson[message.channel.id] = {}
                        cdJson[message.channel.id][msg[1]] = 0
                except:
                    jsonTmp[message.channel.id] = [msg[1]]
                    with open('serverStreamConfig') as jsonLoad:
                        jsonConfig = json.load(jsonLoad)
                    jsonConfig[message.channel.id] = {}
                    jsonConfig[message.channel.id]['imgThumb'] = True
                    jsonConfig[message.channel.id]['ytGaming'] = True
                    jsonConfig[message.channel.id]['mention'] = 'everyone'
                    jsonConfig[message.channel.id]['cooldown'] = 5
                    cdJson[message.channel.id] = {}
                    cdJson[message.channel.id][msg[1]] = 0
                    with open('serverStreamConfig', 'w') as jsonLoad:
                        json.dump(jsonConfig, jsonLoad)
                    print(jsonConfig)
                print(jsonTmp)
                with open('onCooldown', 'w') as jsonfile:
                    json.dump(cdJson, jsonfile)
                with open('serverYTSetup', 'w') as jsonfile:
                    json.dump(jsonTmp, jsonfile)
                await client.send_message(message.channel, 'Channel: \''+msg[1]+'\' added to listener')




            if msg[0].lower() == '!streamcfg':
                with open('serverStreamConfig') as jsonLoad:
                    configJson = json.load(jsonLoad)
                checking = corrector.cmdChecker(msg)
                if not checking:
                    if msg[1] == 'show':
                        await client.send_message(message.channel,
                                        '```Stream config for ' + message.channel.name + ':\n'
                                        '========================================\n'
                                        '\n'
                                        '[imgThumb] | Thumbnail as image: ' + str(configJson[message.channel.id]['imgThumb']) + '\n'
                                        '[ytGaming] | Use Youtube Gaming: ' + str(configJson[message.channel.id]['ytGaming']) + '\n'
                                        '[mention]  | Mention: ' + str(configJson[message.channel.id]['mention']) + '\n'
                                        '[cooldown] | Cooldown if live: ' + str(configJson[message.channel.id]['cooldown']) + ' minutes\n'
                                        '\n'
                                        '========================================\n'
                                        '```'
                                  )
                    elif msg[1] == 'reset':
                        configJson[message.channel.id]['imgThumb'] = True
                        configJson[message.channel.id]['ytGaming'] = True
                        configJson[message.channel.id]['mention'] = 'everyone'
                        configJson[message.channel.id]['cooldown'] = 5
                        with open('serverStreamConfig', 'w') as jsonLoad:
                            json.dump(configJson, jsonLoad)
                        print(configJson)
                        await client.send_message(message.channel, 'Stream config has been reset')
                    elif msg[1] == 'mention':
                        if msg[2].lower() not in ['everyone', 'here', 'none']:
                            await client.send_message(message.channel,
                                        'Incorrect usage: *\''+ msg[0] + ' ' + msg[1] + ' ' + msg[2]+'\'*\n\n'
                                        '```Correct usage:\n'
                                        '==============\n'
                                        '!streamcfg mention [everyone/here/none]\n'
                                        '```'
                                  )
                        else:
                            configJson[message.channel.id]['mention'] = msg[2].lower()
                            with open('serverStreamConfig', 'w') as jsonLoad:
                                json.dump(configJson, jsonLoad)
                            await client.send_message(message.channel,
                                        'Cofig updated!\n'
                                        'New setting: Mention: ' + msg[2].lower()
                                  )
                    elif msg[1] == 'imgThumb':
                        if msg[2].lower() not in ['true', 'false']:
                            await client.send_message(message.channel,
                                        'Incorrect usage: *\'' + msg[0] + ' ' + msg[1] + ' ' + msg[2] + '\'*\n\n'
                                        '```Correct usage:\n'
                                        '==============\n'
                                        '!streamcfg imgThumb [true/false]\n'
                                        '```'
                                  )
                        else:
                            if msg[2].lower() == 'true':
                                configJson[message.channel.id]['imgThumb'] = True
                            else:
                                configJson[message.channel.id]['imgThumb'] = False
                            with open('serverStreamConfig', 'w') as jsonLoad:
                                json.dump(configJson, jsonLoad)
                            await client.send_message(message.channel,
                                        'Cofig updated!\n'
                                        'New setting: Thumnail as image: ' + msg[2].lower()
                                  )
                    elif msg[1] == 'ytGaming':
                        if msg[2].lower() not in ['true', 'false']:
                            await client.send_message(message.channel,
                                        'Incorrect usage: *\'' + msg[0] + ' ' + msg[1] + ' ' + msg[2] + '\'*\n\n'
                                        '```Correct usage:\n'
                                        '==============\n'
                                        '!streamcfg ytGaming [true/false]\n'
                                        '```'
                                  )
                        else:
                            if msg[2].lower() == 'true':
                                configJson[message.channel.id]['ytGaming'] = True
                            else:
                                configJson[message.channel.id]['ytGaming'] = False
                            with open('serverStreamConfig', 'w') as jsonLoad:
                                json.dump(configJson, jsonLoad)
                            await client.send_message(message.channel,
                                        'Cofig updated!\n'
                                        'New setting: Use Youtube Gaming: ' + msg[2].lower()
                                  )
                    elif msg[1] == 'cooldown':
                        if int(float(msg[2])) < 61 and int(float(msg[2])) > 4:
                            configJson[message.channel.id]['cooldown'] = int(float(msg[2]))
                        else:
                            await client.send_message(message.channel,
                                          '```Correct usage:\n'
                                          '==============\n'
                                          '!streamcfg cooldown [5-60]\n'
                                          '```'
                                  )
                    else:
                        await client.send_message(message.channel,
                                        'Incorrect usage: *\'' + message.content + '\'*\n\n'
                                        '```Correct usage:\n'
                                        '==============\n\n'
                                        '!streamcfg [show/reset/ytGaming/imgThumb/mention/cooldown]\n'
                                        '  - ytGaming [true/false]\n'
                                        '  - imgThumb [true/false]\n'
                                        '  - mention  [everyone/here/none]\n'
                                        '  - cooldown [5-60]\n'
                                        '```'
                                  )
                else:
                    await client.send_message(message.channel, checking)

def constCheck(clienter):
    with open('doneAnnounce') as announced:
        content = announced.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    prevLive = [x.strip('\n') for x in content]
    #prevLive = []
    while(True):
        currLive = []
        time.sleep(15)
        with open('onCooldown') as jsonLoad:
            cdJson = json.load(jsonLoad)
        with open('serverStreamConfig') as jsonLoad:
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
                                                          x[1][1] + '***__\" at: https://'+ytG+'youtube.com/watch/?v=' + x[1][2]))
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
            open('doneAnnounce', 'w').close()
            with open('doneAnnounce', 'w') as announced:
                for item in prevLive:
                    announced.write("%s\n" % item)
            with open('onCooldown', 'w') as jsonWrite:
                json.dump(cdJson, jsonWrite)
    return 1

client.run(tokenKeys.discord)
