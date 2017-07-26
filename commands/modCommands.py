import asyncio
import discord
import json

async def checkCommand(message, client):
    msg = message.content.split()
    if msg[0] == "!bannedWords" or msg[0] == "!bw":
        if message.author.permissions_in(message.channel).administrator:
            with open('serverBannedWords') as jsonLoad:
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
                with open('serverBannedWords', 'w') as jsonWrite:
                    json.dump(bWords, jsonWrite)
                await client.send_message(message.channel, "Added new words to the banned list!")
        else:
            await client.send_message(message.channel, "You do not have permission to run this command")

