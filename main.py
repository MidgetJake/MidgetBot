from random import randrange
import discord
import asyncio
import Eball
import botChat

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):

    msg = message.content.split()
    print(message.author.name + " | " + message.content + " | " + message.author.id)

    if len(message.attachments) >= 1:
        await client.add_reaction(message, '👍')
        await client.add_reaction(message, '👎')

    else:
        # Make sure it's not the bot sending the message
        if message.author.id != client.user.id:

            if message.author.id == "276138499554672651" and message.content == "You suck":
                await client.send_message(message.channel, "Not as much as you... " + message.author.mention);

            #If the bot is mentioned repsond with the chatterbot
            if '<@273529250689318923>' in message.content:
                await client.send_message(message.channel, botChat.botChat(message.content))

            # Returns a random number up to the range specified by user
            if message.content.startswith('rand'):
                try:
                    r = int(float(msg[1]))
                    await client.send_message(message.channel, randrange(r))
                except ValueError:
                    await client.send_message(message.channel, 'The second word must be a number')
                except IndexError:
                    await client.send_message(message.channel, 'A number is required')

            # Sah dude
            if message.content.lower().startswith('sah'):
                await client.send_message(message.channel, 'Sah dude')

            # Respond to some rude remarks
            if (msg[0].lower() == 'fuck') and (msg[1].lower() == 'you'):
                await client.send_message(message.channel, 'Fuck you too ' + message.author.mention)

            # The wisdom of 8ball is great!
            if msg[0].lower() == '8ball':
                await client.send_message(message.channel, Eball.eBall(randrange(16)))

#Gotta hide the token!
client.run('######')
