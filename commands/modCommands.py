# Todo:
#       - Detect role in server and allow mods to assign roles to commands
#       - !muteall <user> | Mute a user in all channels
#       - !slowall <time> | Enable slowmode in all channels
#       - !timeout <user> <seconds> | Mutes user for a period of time
#       - !clear <no. messages> | Deletes the last number of messages
#       - !bannedWords remove <[words]> | Allow banned words to be removed

from commands.helpers import checkJson
import json

async def checkCommand(message, client):
    if message.author.permissions_in(message.channel).administrator:
        msg = message.content.split()
        try:
            if msg[0] == "!bannedWords" or msg[0] == "!bw":
                with open('config/serverHardBannedWords') as jsonLoad:
                    hBWords = json.load(jsonLoad)
                try:
                    hBList = hBWords[message.server.id]
                except KeyError:
                    hBList = []

                with open('config/serverSoftBannedWords') as jsonLoad:
                    sBWords = json.load(jsonLoad)
                try:
                    sBList = sBWords[message.server.id]
                except KeyError:
                    sBList = []

                if msg[1] == "show":
                    pass
                    #await client.send_message(message.channel, bList)
                elif msg[1] == "-a":
                    if msg[2] == "-h":
                        addWords = msg[3::]
                        hBList = hBList + addWords
                        hBWords[message.server.id] = hBList
                        with open('config/serverHardBannedWords', 'w') as jsonWrite:
                            json.dump(hBWords, jsonWrite)
                        #await client.send_message(message.channel, "Added new words to the banned list!")
                    else:
                        addWords = msg[2::]
                        sBList = sBList + addWords
                        sBWords[message.server.id] = sBList
                        with open('config/serverSoftBannedWords', 'w') as jsonWrite:
                            json.dump(sBWords, jsonWrite)

            if msg[0] == "!slow" or msg[0] == "!slowmode":
                with open('config/serverSettings', 'r') as rf:
                    sSettings = json.load(rf)

                if msg[1].lower() == 'off':
                    sSettings = checkJson(sSettings, 'slowMode', message, False)
                    sSettings = checkJson(sSettings, 'slowTime', message, 0)
                    await client.send_message(message.channel, 'Slow mode is now disabled')
                else:
                    try:
                        slowTime = int(float(msg[1]))
                        sSettings = checkJson(sSettings, 'slowMode', message, True)
                        sSettings = checkJson(sSettings, 'slowTime', message, slowTime)
                        with open('slowModeChannels', 'r') as rf:
                            slowChan = json.load(rf)
                        slowChan[message.channel.id] = {}
                        with open('slowModeChannels', 'w') as wf:
                            json.dump(slowChan, wf)
                        await client.send_message(message.channel, 'Slow mode is now enabled with a timer of: ' + msg[1] + ' seconds!')
                    except:
                        pass
                with open('config/serverSettings', 'w') as wf:
                    json.dump(sSettings, wf)

            if msg[0] == '!mute':
                with open('config/mutedUsers', 'r') as rf:
                    mUsers = json.load(rf)

                for user in message.mentions:
                    mUsers = checkJson(mUsers, user.id, message, True)

                with open('config/mutedUsers', 'w') as wf:
                    json.dump(mUsers, wf)

            if msg[0] == '!unmute':
                with open('config/mutedUsers', 'r') as rf:
                    mUsers = json.load(rf)

                for user in message.mentions:
                    mUsers = checkJson(mUsers, user.id, message, False)

                with open('config/mutedUsers', 'w') as wf:
                    json.dump(mUsers, wf)
        except:
            pass
