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
import autoMod

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
            if msg[0] == "!bannedWords" or msg[0] == "!bw":
                if(message.author.permissions_in(message.channel).administrator):
                    with open('serverBannedWords') as jsonLoad:
                        bWords = json.load(jsonLoad)
                    try:
                        bList = bWords[message.server.id][message.channel.id]
                        chanAvail = True
                    except:
                        chanAvail = False
                        bList = []

                    if msg[1] == "show":
                        await client.send_message(message.channel, bList)
                    elif msg[1] == "add":
                        addWords = msg[2::]
                        bList = bList + addWords
                        if chanAvail:
                            bWords[message.server.id][message.channel.id] = bList
                        else:
                            try:
                                bWords[message.server.id][message.channel.id] = bList
                            except:
                                bWords[message.server.id] = {}
                                bWords[message.server.id][message.channel.id] = bList
                        with open('serverBannedWords', 'w') as jsonWrite:
                            json.dump(bWords, jsonWrite)
                        await client.send_message(message.channel, "Added new words to the banned list!")
                else:
                    await client.send_message(message.channel, "You do not have permission to run this command")

            if autoMod.doChecks(message):
                await client.delete_message(message)
            else:
                if message.author.id == '95677195162222592' and msg[0] == '!debug':
                    for chan in message.server.channels:
                        print(chan)

                if msg[0] == "!discordPromo" or msg[0] == "!dp":
                    if (message.author.permissions_in(message.channel).administrator):
                        with open('serverSettings') as jsonLoad:
                            sSetting = json.load(jsonLoad)
                        if msg[1].lower() == "enable":
                            try:
                                sSetting[message.server.id][message.channel.id]['canPromoteDiscord'] = True
                            except:
                                try:
                                    sSetting[message.server.id][message.channel.id]['canPromoteDiscord'] = True
                                except:
                                    try:
                                        sSetting[message.server.id][message.channel.id] = {}
                                        sSetting[message.server.id][message.channel.id]['canPromoteDiscord'] = True
                                    except:
                                        sSetting[message.server.id] = {}
                                        sSetting[message.server.id][message.channel.id] = {}
                                        sSetting[message.server.id][message.channel.id]['canPromoteDiscord'] = True
                            with open('serverSettings', 'w') as jsonWrite:
                                json.dump(sSetting, jsonWrite)
                            await client.send_message(message.channel, "Promotion of discord servers is now enabled in this channel")
                        elif msg[1].lower() == "disable":
                            try:
                                sSetting[message.server.id][message.channel.id]['canPromoteDiscord'] = False
                            except:
                                try:
                                    sSetting[message.server.id][message.channel.id]['canPromoteDiscord'] = False
                                except:
                                    try:
                                        sSetting[message.server.id][message.channel.id] = {}
                                        sSetting[message.server.id][message.channel.id]['canPromoteDiscord'] = False
                                    except:
                                        sSetting[message.server.id] = {}
                                        sSetting[message.server.id][message.channel.id] = {}
                                        sSetting[message.server.id][message.channel.id]['canPromoteDiscord'] = False
                            with open('serverSettings', 'w') as jsonWrite:
                                json.dump(sSetting, jsonWrite)
                            await client.send_message(message.channel, "Promotion of discord servers is now disabled in this channel")
                        elif msg[1].lower() == "all":
                            if msg[2].lower() == "enable":
                                valid = True
                                chge = True
                            elif msg[2].lower() == "disable":
                                valid = True
                                chge = False
                            else:
                                valid = False

                            if valid:
                                for cha in message.server.channels:
                                    print(cha.type)
                                    if cha.type == discord.ChannelType.text:
                                        try:
                                            sSetting[message.server.id][cha.id]['canPromoteDiscord'] = chge
                                        except:
                                            try:
                                                sSetting[message.server.id][cha.id]['canPromoteDiscord'] = chge
                                            except:
                                                try:
                                                    sSetting[message.server.id][cha.id] = {}
                                                    sSetting[message.server.id][cha.id]['canPromoteDiscord'] = chge
                                                except:
                                                    sSetting[message.server.id] = {}
                                                    sSetting[message.server.id][cha.id] = {}
                                                    sSetting[message.server.id][cha.id]['canPromoteDiscord'] = chge
                                with open('serverSettings', 'w') as jsonWrite:
                                    json.dump(sSetting, jsonWrite)


                if msg[0] == "!chatBot" or msg[0] == "!cb":
                    if (message.author.permissions_in(message.channel).administrator):
                        with open('serverSettings') as jsonLoad:
                            cbChan = json.load(jsonLoad)
                        if msg[1].lower() == 'enable':
                            try:
                                cbChan[message.server.id][message.channel.id]['canChatBot'] = True
                            except:
                                try:
                                    cbChan[message.server.id][message.channel.id] = {}
                                    cbChan[message.server.id][message.channel.id]['canChatBot'] = True
                                except:
                                    cbChan[message.server.id] = {}
                                    cbChan[message.server.id][message.channel.id] = {}
                                    cbChan[message.server.id][message.channel.id]['canChatBot'] = True
                        elif msg[1].lower() == 'disable':
                            try:
                                cbChan[message.server.id][message.channel.id]['canChatBot'] = False
                            except:
                                try:
                                    cbChan[message.server.id][message.channel.id] = {}
                                    cbChan[message.server.id][message.channel.id]['canChatBot'] = False
                                except:
                                    cbChan[message.server.id] = {}
                                    cbChan[message.server.id][message.channel.id] = {}
                                    cbChan[message.server.id][message.channel.id]['canChatBot'] = False
                        with open('serverSettings', 'w') as jsonWrite:
                            json.dump(cbChan, jsonWrite)

                if msg[0] == "!ytProm" or msg[0] == "!ytp":
                    if (message.author.permissions_in(message.channel).administrator):
                        with open('serverSettings') as jsonLoad:
                            sSettings = json.load(jsonLoad)
                        if msg[1].lower() == 'enable':
                            try:
                                sSettings[message.server.id][message.channel.id]['canPromoteYT'] = True
                            except:
                                try:
                                    sSettings[message.server.id][message.channel.id] = {}
                                    sSettings[message.server.id][message.channel.id]['canPromoteYT'] = True
                                except:
                                    sSettings[message.server.id] = {}
                                    sSettings[message.server.id][message.channel.id] = {}
                                    sSettings[message.server.id][message.channel.id]['canPromoteYT'] = True
                        elif msg[1].lower() == 'disable':
                            try:
                                sSettings[message.server.id][message.channel.id]['canPromoteYT'] = False
                            except:
                                try:
                                    sSettings[message.server.id][message.channel.id] = {}
                                    sSettings[message.server.id][message.channel.id]['canPromoteYT'] = False
                                except:
                                    sSettings[message.server.id] = {}
                                    sSettings[message.server.id][message.channel.id] = {}
                                    sSettings[message.server.id][message.channel.id]['canPromoteYT'] = False
                        #print(sSettings[message.server.id][message.channel.id]['canPromoteYT'])
                        elif msg[1].lower() == "all":
                            if msg[2].lower() == "enable":
                                valid = True
                                chge = True
                            elif msg[2].lower() == "disable":
                                valid = True
                                chge = False
                            else:
                                valid = False

                            if valid:
                                for cha in message.server.channels:
                                    print(cha.type)
                                    if cha.type == discord.ChannelType.text:
                                        try:
                                            sSettings[message.server.id][cha.id]['canPromoteYT'] = chge
                                        except:
                                            try:
                                                sSettings[message.server.id][cha.id]['canPromoteYT'] = chge
                                            except:
                                                try:
                                                    sSettings[message.server.id][cha.id] = {}
                                                    sSettings[message.server.id][cha.id]['canPromoteYT'] = chge
                                                except:
                                                    sSettings[message.server.id] = {}
                                                    sSettings[message.server.id][cha.id] = {}
                                                    sSettings[message.server.id][cha.id]['canPromoteYT'] = chge
                        with open('serverSettings', 'w') as jsonWrite:
                            json.dump(sSettings, jsonWrite)


                #If the bot is mentioned repsond with the chatterbot
                if '<@273529250689318923>' in message.content:
                    with open('serverSettings') as jsonLoad:
                        cbChan = json.load(jsonLoad)
                    try:
                        chatIn = cbChan[message.server.id][message.channel.id]['canChatBot']
                    except:
                        chatIn = True
                    print(chatIn)
                    if chatIn:
                        await client.send_message(message.channel, botChat.botChat(message.content))

                # Returns a random number up to the range specified by user
                if msg[0] == '!rand':
                    try:
                        r = int(float(msg[1]))
                        await client.send_message(message.channel, randrange(r))
                    except ValueError:
                        await client.send_message(message.channel, 'The second argument must be a number')
                    except IndexError:
                        await client.send_message(message.channel, 'A number is required')

                # The wisdom of 8ball is great!
                if msg[0].lower() == '8ball':
                    await client.send_message(message.channel, Eball.eBall(randrange(16)))


                #Because of limited api calls only I can create a youtube stream listener
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
            open('doneAnnounce', 'w').close()
            with open('doneAnnounce', 'w') as announced:
                for item in prevLive:
                    announced.write("%s\n" % item)
            with open('onCooldown', 'w') as jsonWrite:
                json.dump(cdJson, jsonWrite)
    return 1

client.run(tokenKeys.discord)
