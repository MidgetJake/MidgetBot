from chatterbotapi import ChatterBotFactory, ChatterBotType
from ExpChatBot import chat
import json

async def checkCommand(message, client):
    msg = message.content.split()
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
            elif msg[1].lower() == 'exp':
                if msg[2].lower() == 'enable':
                    try:
                        cbChan[message.server.id][message.channel.id]['expChatBot'] = True
                    except:
                        try:
                            cbChan[message.server.id][message.channel.id] = {}
                            cbChan[message.server.id][message.channel.id]['expChatBot'] = True
                        except:
                            cbChan[message.server.id] = {}
                            cbChan[message.server.id][message.channel.id] = {}
                            cbChan[message.server.id][message.channel.id]['expChatBot'] = True
                elif msg[2].lower() == 'disable':
                    try:
                        cbChan[message.server.id][message.channel.id]['expChatBot'] = False
                    except:
                        try:
                            cbChan[message.server.id][message.channel.id] = {}
                            cbChan[message.server.id][message.channel.id]['expChatBot'] = False
                        except:
                            cbChan[message.server.id] = {}
                            cbChan[message.server.id][message.channel.id] = {}
                            cbChan[message.server.id][message.channel.id]['expChatBot'] = False
            with open('serverSettings', 'w') as jsonWrite:
                json.dump(cbChan, jsonWrite)

async def chatBotTalk(message, client):
    # If the bot is mentioned repsond with the chatterbot
    if '<@273529250689318923>' in message.content:
        with open('serverSettings') as jsonLoad:
            cbChan = json.load(jsonLoad)
        try:
            chatIn = cbChan[message.server.id][message.channel.id]['canChatBot']
        except:
            chatIn = True
        try:
            expChat = cbChan[message.server.id][message.channel.id]['expChatBot']
        except:
            expChat = False
        print("---")
        print(chatIn)
        print(expChat)
        print("---")
        if chatIn:
            if expChat:
                await client.send_message(message.channel, chat.takeMsg(message.content))
            else:
                await client.send_message(message.channel, botChat(message.content))







def botChat(message):
    factory = ChatterBotFactory()
    bot = factory.create(ChatterBotType.PANDORABOTS, "b0dafd24ee35a477")
    bot2session = bot.create_session()
    send = message.strip('<@273529250689318923>')
    if not send:
        return "Don't give me silence..."
    else:
        return bot2session.think(send)