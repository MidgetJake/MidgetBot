import json
from time import time
from config import bannedWords
from commands.helpers import checkJson


def doChecks(msg):
    if not msg.author.permissions_in(msg.channel).administrator:
        checkList = []
        checkList.append(isMuted(msg))
        checkList.append(slowMode(msg))
        checkList.append(checkIfBanned(msg))
        checkList.append(checkForDiscordProm(msg))
        checkList.append(checkForYoutube(msg))
        print(checkList)
        if True in checkList:
            return True
        else:
            return False

def checkIfBanned(msg):
    with open('config/serverHardBannedWords') as jsonLoad:
        hardBWords = json.load(jsonLoad)

    with open('config/serverSoftBannedWords') as jsonLoad:
        softBWords = json.load(jsonLoad)

    with open('config/serverSettings') as jsonLoad:
        sSetting = json.load(jsonLoad)

    try:
        hardBList = hardBWords[msg.server.id]
    except:
        hardBList = []

    try:
        softBList = softBWords[msg.server.id]
    except:
        softBList = []

    try:
        if sSetting[msg.server.id][msg.channel.id]["preSetBannedWords"] == True:
            softBList = softBList + bannedWords.defaultBans
    except:
        pass

    for bWord in hardBList:
        if bWord in msg.content.lower():
            return True

    msgSplit = msg.content.split()

    for word in msgSplit:
        if word.lower() in softBList:
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

def slowMode(msg):
    with open('config/serverSettings', 'r') as rf:
        sSettings = json.load(rf)

    try:
        isSlow = sSettings[msg.server.id][msg.channel.id]['slowMode']
    except:
        sSettings = checkJson(sSettings, 'slowMode', msg, False)
        sSettings = checkJson(sSettings, 'slowTime', msg, 0)
        isSlow = False

    if isSlow:
        sTime = sSettings[msg.server.id][msg.channel.id]['slowTime']
        with open('config/slowModeChannels', 'r') as rf:
            slowChan = json.load(rf)
        try:
            if time() - (slowChan[msg.channel.id][msg.author.id] + sTime) > 0:
                slowChan[msg.channel.id][msg.author.id] = time()
            else:
                print('Deleting message')
                return True
        except:
            try:
                slowChan[msg.channel.id][msg.author.id] = time()
            except:
                slowChan[msg.channel.id] = {}
                slowChan[msg.channel.id][msg.author.id] = time()
        with open('config/slowModeChannels', 'w') as wf:
            json.dump(slowChan, wf)
    return False

def isMuted(msg):
    with open('config/mutedUsers', 'r') as rf:
        mUsers = json.load(rf)

    try:
        if mUsers[msg.server.id][msg.channel.id][msg.author.id]:
            return True
        else:
            return False
    except:
        return False