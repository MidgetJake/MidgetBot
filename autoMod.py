import discord
import json
import bannedWords

def doChecks(msg):
    checkList = []
    checkList.append(checkIfBanned(msg))
    checkList.append(checkForDiscordProm(msg))
    print(checkList)
    if True in checkList:
        return True
    else:
        return False

def checkIfBanned(msg):
    with open('serverBannedWords') as jsonLoad:
        bWords = json.load(jsonLoad)

    with open('serverSettings') as jsonLoad:
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
    with open('serverSettings') as jsonLoad:
        sSetting = json.load(jsonLoad)

    try:
        canProm = sSetting[msg.server.id][msg.channel.id]['canPromoteDiscord'] = True
    except:
        try:
            sSetting[msg.server.id][msg.channel.id]['canPromoteDiscord'] = True
        except:
            try:
                sSetting[msg.server.id][msg.channel.id] = {}
                sSetting[msg.server.id][msg.channel.id]['canPromoteDiscord'] = True
            except:
                sSetting[msg.server.id] = {}
                sSetting[msg.server.id][msg.channel.id] = {}
                sSetting[msg.server.id][msg.channel.id]['canPromoteDiscord'] = True
        with open('serverSettings', 'w') as jsonWrite:
            json.dump(sSetting, jsonWrite)
        canProm = True

    if not canProm:
        if "discord.gg/" in msg.content:
            if (msg.author.permissions_in(msg.channel).administrator):
                return False
            else:
                return True

    return False
