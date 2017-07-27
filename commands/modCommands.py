from commands.helpers import checkJson
import json

async def checkCommand(message, client):
    if message.author.permissions_in(message.channel).administrator:
        msg = message.content.split()
        if msg[0] == "!bannedWords" or msg[0] == "!bw":
            with open('config/serverBannedWords') as jsonLoad:
                bWords = json.load(jsonLoad)
            try:
                bList = bWords[message.server.id][message.channel.id]
                chanAvail = True
            except KeyError:
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
                with open('config/serverBannedWords', 'w') as jsonWrite:
                    json.dump(bWords, jsonWrite)
                await client.send_message(message.channel, "Added new words to the banned list!")

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
                    await client.send_message(message.channel, 'Slow mode is now enabled with a timer of: ' + msg[1] + ' seconds!')
                except:
                    pass
            with open('config/serverSettings', 'w') as wf:
                json.dump(sSettings, wf)


