import json

from config import bannedWords


def doChecks(msg):
    checkList = []
    checkList.append(checkIfBanned(msg))
    checkList.append(checkForDiscordProm(msg))
    checkList.append(checkForYoutube(msg))
    print(checkList)
    if True in checkList:
        return True
    else:
        return False

def checkIfBanned(msg):
    with open('config/serverBannedWords') as jsonLoad:
        bWords = json.load(jsonLoad)

    with open('config/serverSettings') as jsonLoad:
        sSetting = json.load(jsonLoad)

    try:
        bList = bWords[msg.server.id][msg.channel.id]
    except:
        bList = []

    try:
        if sSetting[msg.server.id][msg.channel.id]["preSetBannedWords"] == True:
            bList = bList + bannedWords.defaultBans
    except:
        pass

    msgSplit = msg.content.split()

    for word in msgSplit:
        if word.lower() in bList:
            try:
                print("Deleting: " + msg.content)
                return True
            except:
                return True

    return False

def checkForDiscordProm(msg):
    with open('config/serverSettings') as jsonLoad:
        sSetting = json.load(jsonLoad)

    try:
        canProm = sSetting[msg.server.id][msg.channel.id]['canPromoteDiscord']
    except:
        try:
            sSetting[msg.server.id][msg.channel.id] = {}
            sSetting[msg.server.id][msg.channel.id]['canPromoteDiscord'] = True
        except:
            sSetting[msg.server.id] = {}
            sSetting[msg.server.id][msg.channel.id] = {}
            sSetting[msg.server.id][msg.channel.id]['canPromoteDiscord'] = True
        with open('config/serverSettings', 'w') as jsonWrite:
            json.dump(sSetting, jsonWrite)
        canProm = True

    if not canProm:
        if 'discord.gg/' in msg.content:
            if (msg.author.permissions_in(msg.channel).administrator):
                print('Admin can do this k?')
                return False
            else:
                return True

    return False

def checkForYoutube(msg):
    with open('config/serverSettings') as jsonLoad:
        sSetting = json.load(jsonLoad)

    try:
        canProm = sSetting[msg.server.id][msg.channel.id]['canPromoteYT']
    except:
        try:
            sSetting[msg.server.id][msg.channel.id] = {}
            sSetting[msg.server.id][msg.channel.id]['canPromoteYT'] = True
        except:
            sSetting[msg.server.id] = {}
            sSetting[msg.server.id][msg.channel.id] = {}
        with open('config/serverSettings', 'w') as jsonWrite:
            json.dump(sSetting, jsonWrite)
        canProm = True
    if not canProm:
        if 'youtube.com/' in msg.content or 'youtu.be/' in msg.content:
            if 'user' in msg.content or '.com/c' in msg.content:
                if (msg.author.permissions_in(msg.channel).administrator):
                    print('Admin can do this k?')
                    return False
                else:
                    return True
        return False
