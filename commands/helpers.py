
# This was copy-pasted all over the place so may aswell make it a helper function
def checkJson(jsonVar, varName, message, output):
    try:
        jsonVar[message.server.id][message.channel.id][varName] = output
    except:
        try:
            jsonVar[message.server.id][message.channel.id] = {}
            jsonVar[message.server.id][message.channel.id][varName] = output
        except:
            jsonVar[message.server.id] = {}
            jsonVar[message.server.id][message.channel.id] = {}
            jsonVar[message.server.id][message.channel.id][varName] = output
    return jsonVar