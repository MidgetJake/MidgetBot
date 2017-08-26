# Todo:
#       - Detect role in server and allow mods to assign roles to commands
#       - !muteall <user> | Mute a user in all channels
#       - !slowall <time> | Enable slowmode in all channels
#       - !timeout <user> <seconds> | Mutes user for a period of time
#       - !clear <no. messages> | Deletes the last number of messages
#       - !bannedWords remove <[words]> | Allow banned words to be removed
from modules.helpers import checkJson
import psycopg2 as postG
from config import tokenKeys
import json
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

host = tokenKeys.dbHost
user = tokenKeys.dbUser
passW = tokenKeys.dbPass


async def commandHandler(message, client):
    if message.author.permissions_in(message.channel).administrator:
        msg = message.content.split()
        if msg[0] in ['!roleperms', '!rp']:
            await rolePerms(message, client)
        elif msg[0] in ['!bannedwords', '!bw']:
            await bannedWords(message),
        elif msg[0] in ['!slow']:
            await slowMode(message, client)
        elif msg[0] in ['!mute']:
            await muteToggle(message, True)
        elif msg[0] in ['!unmute']:
            await muteToggle(message, False)




async def rolePerms(message, client):
    msg = message.content.split()
    if msg[1] == 'list':
        try:
            roleNum = int(msg[2])
            permList = client.serverDict[message.server.id].rolePerms
            permList = permList[message.server.roles[roleNum].name]
            permStr = '```'
            permCnt = 0
            for key, value in permList.items():
                permStr += '[{}] | {} - {}\n'.format(permCnt, key, value)
                permCnt += 1
            permStr += '```'
            await client.send_message(message.channel, permStr)
        except:
            roleStr = '```'
            rCnt = 0
            for role in message.server.roles:
                roleStr += '[{}] - {}\n'.format(rCnt, role.name)
                rCnt += 1
            roleStr += '```'
            await client.send_message(message.channel, roleStr)
    elif msg[1] == 'edit':
        try:
            roleNum = int(msg[2])
            permName = ['slow', 'mute', 'banword', 'timeout', 'clear', 'addquote', 'editquote', 'delquote'][int(msg[3])]
            permVal = {
                         'true': True,
                         'false': False
                      }.get(msg[4].lower())
            upTuple = (roleNum, permName, permVal)
            updateRolePerms(message, client, upTuple)
        except:
            await client.send_message(message.channel, '```You must enter a role number, permission number and value\n'
                                                       ' - Structured like this: \"!roleperm edit <role num> <perm num> <true/false>\"\n'
                                                       ' - To see role numbers try \"!roleperms list\"\n'
                                                       ' - To see permission numbers try: \"!roleperms list <role number>\"\n'
                                                       ' - The value will always be \"true\" or \"false\"```')
    return True

def updateRolePerms(message, client, updateTup):
    role = message.server.roles[updateTup[0]].name
    perm = updateTup[1]
    newVal = updateTup[2]

    test = 'server_{}'.format(message.server.id)
    conn_string = 'host = {} dbname = {} user = {} password = {}'.format(host, test, user, passW)
    conn = postG.connect(conn_string)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute('UPDATE roleperms SET {} = %s WHERE name = %s'.format(perm), (newVal, role))
    client.serverDict[message.server.id].getRolePerms()
    print('| Role: {} was updated - {} = {}'.format(role, perm, newVal))

async def bannedWords(message):
    print('| !bw command was run')
    msg = message.content.split()
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
        # await client.send_message(message.channel, bList)
    elif msg[1] == "-a":
        if msg[2] == "-h":
            addWords = msg[3::]
            hBList = hBList + addWords
            hBWords[message.server.id] = hBList
            with open('config/serverHardBannedWords', 'w') as jsonWrite:
                json.dump(hBWords, jsonWrite)
                # await client.send_message(message.channel, "Added new words to the banned list!")
        else:
            addWords = msg[2::]
            sBList = sBList + addWords
            sBWords[message.server.id] = sBList
            with open('config/serverSoftBannedWords', 'w') as jsonWrite:
                json.dump(sBWords, jsonWrite)
    return True


async def slowMode(message, client):
    print('| !slow command was run')
    msg = message.content.split()
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
            await client.send_message(message.channel,
                                      'Slow mode is now enabled with a timer of: ' + msg[1] + ' seconds!')
        except:
            pass
    with open('config/serverSettings', 'w') as wf:
        json.dump(sSettings, wf)
    return True


async def muteToggle(message, mute):
    print('| !mute command was run')
    if mute:
        with open('config/mutedUsers', 'r') as rf:
            mUsers = json.load(rf)

        for user in message.mentions:
            mUsers = checkJson(mUsers, user.id, message, True)

        with open('config/mutedUsers', 'w') as wf:
            json.dump(mUsers, wf)
    else:
        with open('config/mutedUsers', 'r') as rf:
            mUsers = json.load(rf)

        for user in message.mentions:
            mUsers = checkJson(mUsers, user.id, message, False)

        with open('config/mutedUsers', 'w') as wf:
            json.dump(mUsers, wf)
    return True


"""
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
            pass"""
