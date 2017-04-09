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
            if message.content.startswith('rand'):
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
                with open('serverYTSetup') as jsonfile:
                    jsonTmp = json.load(jsonfile)
                try:
                    jsonTmp[message.channel.id].append(msg[1])
                except:
                    jsonTmp[message.channel.id] = [msg[1]]
                print(jsonTmp)
                #jsonTmp = '{\"'+message.channel.id+'\": [\"'+msg[1]+'\"]}'
                with open('serverYTSetup', 'w') as jsonfile:
                    json.dump(jsonTmp, jsonfile)
                await client.send_message(message.channel, 'Channel: \''+msg[1]+'\' added to listener')

def constCheck(clienter):
    timeCheck = 0
    prevLive = []
    while(True):
        currLive = []
        chanList = youtubeChecker.findLiveChans(timeCheck)
        if timeCheck > 5000000:
            timeCheck = 0
        if chanList != []:
            for x in chanList:
                currLive.append(x[1])
                if x[1] in prevLive:
                    pass
                else:
                    prevLive.append(x[1])
                    youtubeChecker.getLiveThumbnail(x[1])
                    coro = clienter.send_file(discord.Object(id=x[0]), 'temp.jpg', content=('@everyone | '+youtubeChecker.getChanName(x[1]) + ' is now streaming: \"__***'+youtubeChecker.getLiveTitle(x[1])+'***__\" at: https://gaming.youtube.com/watch/?v='+youtubeChecker.getLiveLink(x[1])))
                    fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
                    try:
                        fut.result()
                    except:
                        print("There was an issue with the thread")
            newPrevLive = []
            for vid in prevLive:
                if vid in currLive and vid not in newPrevLive:
                    newPrevLive.append(vid)
                else:
                    pass
            prevLive = newPrevLive
        timeCheck += 1
    return 1

client.run(tokenKeys.discord)
