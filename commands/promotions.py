import discord
import json

async def checkCommand(message, client):
    msg = message.content.split()
    if msg[0] == "!discordPromo" or msg[0] == "!dp":
        if message.author.permissions_in(message.channel).administrator:
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
            # print(sSettings[message.server.id][message.channel.id]['canPromoteYT'])
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