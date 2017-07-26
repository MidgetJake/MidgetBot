import json
import corrector

async def checkCommand(message, client):
    msg = message.content.split()
    #Because of limited api calls only I can create a youtube stream listener
    if message.author.id == '95677195162222592' and msg[0].lower() == '!setupyt':
        with open('onCooldown') as jsonLoad:
            cdJson = json.load(jsonLoad)
        with open('serverYTSetup') as jsonfile:
            jsonTmp = json.load(jsonfile)
        try:
            jsonTmp[message.channel.id].append(msg[1])
            try:
                cdJson[message.channel.id][msg[1]] = 0
            except:
                cdJson[message.channel.id] = {}
                cdJson[message.channel.id][msg[1]] = 0
        except:
            jsonTmp[message.channel.id] = [msg[1]]
            with open('serverStreamConfig') as jsonLoad:
                jsonConfig = json.load(jsonLoad)
            jsonConfig[message.channel.id] = {}
            jsonConfig[message.channel.id]['imgThumb'] = True
            jsonConfig[message.channel.id]['ytGaming'] = True
            jsonConfig[message.channel.id]['mention'] = 'everyone'
            jsonConfig[message.channel.id]['cooldown'] = 5
            cdJson[message.channel.id] = {}
            cdJson[message.channel.id][msg[1]] = 0
            with open('serverStreamConfig', 'w') as jsonLoad:
                json.dump(jsonConfig, jsonLoad)
            print(jsonConfig)
        print(jsonTmp)
        with open('onCooldown', 'w') as jsonfile:
            json.dump(cdJson, jsonfile)
        with open('serverYTSetup', 'w') as jsonfile:
            json.dump(jsonTmp, jsonfile)
        await client.send_message(message.channel, 'Channel: \''+msg[1]+'\' added to listener')




    if msg[0].lower() == '!streamcfg':
        with open('serverStreamConfig') as jsonLoad:
            configJson = json.load(jsonLoad)
        checking = corrector.cmdChecker(msg)
        if not checking:
            if msg[1] == 'show':
                await client.send_message(message.channel,
                                '```Stream config for ' + message.channel.name + ':\n'
                                '========================================\n'
                                '\n'
                                '[imgThumb] | Thumbnail as image: ' + str(configJson[message.channel.id]['imgThumb']) + '\n'
                                '[ytGaming] | Use Youtube Gaming: ' + str(configJson[message.channel.id]['ytGaming']) + '\n'
                                '[mention]  | Mention: ' + str(configJson[message.channel.id]['mention']) + '\n'
                                '[cooldown] | Cooldown if live: ' + str(configJson[message.channel.id]['cooldown']) + ' minutes\n'
                                '\n'
                                '========================================\n'
                                '```'
                          )
            elif msg[1] == 'reset':
                configJson[message.channel.id]['imgThumb'] = True
                configJson[message.channel.id]['ytGaming'] = True
                configJson[message.channel.id]['mention'] = 'everyone'
                configJson[message.channel.id]['cooldown'] = 5
                with open('serverStreamConfig', 'w') as jsonLoad:
                    json.dump(configJson, jsonLoad)
                print(configJson)
                await client.send_message(message.channel, 'Stream config has been reset')
            elif msg[1] == 'mention':
                if msg[2].lower() not in ['everyone', 'here', 'none']:
                    await client.send_message(message.channel,
                                'Incorrect usage: *\''+ msg[0] + ' ' + msg[1] + ' ' + msg[2]+'\'*\n\n'
                                '```Correct usage:\n'
                                '==============\n'
                                '!streamcfg mention [everyone/here/none]\n'
                                '```'
                          )
                else:
                    configJson[message.channel.id]['mention'] = msg[2].lower()
                    with open('serverStreamConfig', 'w') as jsonLoad:
                        json.dump(configJson, jsonLoad)
                    await client.send_message(message.channel,
                                'Cofig updated!\n'
                                'New setting: Mention: ' + msg[2].lower()
                          )
            elif msg[1] == 'imgThumb':
                if msg[2].lower() not in ['true', 'false']:
                    await client.send_message(message.channel,
                                'Incorrect usage: *\'' + msg[0] + ' ' + msg[1] + ' ' + msg[2] + '\'*\n\n'
                                '```Correct usage:\n'
                                '==============\n'
                                '!streamcfg imgThumb [true/false]\n'
                                '```'
                          )
                else:
                    if msg[2].lower() == 'true':
                        configJson[message.channel.id]['imgThumb'] = True
                    else:
                        configJson[message.channel.id]['imgThumb'] = False
                    with open('serverStreamConfig', 'w') as jsonLoad:
                        json.dump(configJson, jsonLoad)
                    await client.send_message(message.channel,
                                'Cofig updated!\n'
                                'New setting: Thumnail as image: ' + msg[2].lower()
                          )
            elif msg[1] == 'ytGaming':
                if msg[2].lower() not in ['true', 'false']:
                    await client.send_message(message.channel,
                                'Incorrect usage: *\'' + msg[0] + ' ' + msg[1] + ' ' + msg[2] + '\'*\n\n'
                                '```Correct usage:\n'
                                '==============\n'
                                '!streamcfg ytGaming [true/false]\n'
                                '```'
                          )
                else:
                    if msg[2].lower() == 'true':
                        configJson[message.channel.id]['ytGaming'] = True
                    else:
                        configJson[message.channel.id]['ytGaming'] = False
                    with open('serverStreamConfig', 'w') as jsonLoad:
                        json.dump(configJson, jsonLoad)
                    await client.send_message(message.channel,
                                'Cofig updated!\n'
                                'New setting: Use Youtube Gaming: ' + msg[2].lower()
                          )
            elif msg[1] == 'cooldown':
                if int(float(msg[2])) < 61 and int(float(msg[2])) > 4:
                    configJson[message.channel.id]['cooldown'] = int(float(msg[2]))
                else:
                    await client.send_message(message.channel,
                                  '```Correct usage:\n'
                                  '==============\n'
                                  '!streamcfg cooldown [5-60]\n'
                                  '```'
                          )
            else:
                await client.send_message(message.channel,
                                'Incorrect usage: *\'' + message.content + '\'*\n\n'
                                '```Correct usage:\n'
                                '==============\n\n'
                                '!streamcfg [show/reset/ytGaming/imgThumb/mention/cooldown]\n'
                                '  - ytGaming [true/false]\n'
                                '  - imgThumb [true/false]\n'
                                '  - mention  [everyone/here/none]\n'
                                '  - cooldown [5-60]\n'
                                '```'
                          )
        else:
            await client.send_message(message.channel, checking)