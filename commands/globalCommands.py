from random import randrange
import Eball


async def checkCommand(message, client):

    msg = message.content.split()
    # The wisdom of 8ball is great!
    if msg[0].lower() == '!8ball':
        await client.send_message(message.channel, Eball.eBall(randrange(20)))

    # Returns a random number up to the range specified by user
    #if msg[0] == '!rand':
    #    try:
    #        r = int(float(msg[1]))
    #        await client.send_message(message.channel, randrange(r))
    #    except ValueError:
    #        await client.send_message(message.channel, 'The second argument must be a number')
    #    except IndexError:
    #        await client.send_message(message.channel, 'A number is required')