# This is all just experimental and won't be worked on too much currently
# We are using this to save time/resources as calling the database for EVERY message can potentially be slow
# Although it is still very WiP

####################
# The server class #
####################
class Server:
    def __init__(self, server):
        self.server = server
        self.id = server.id
        self.channels = []
        for channel in server.channels:
            self.addChannel(channel)
        print('Server: {} now initialised'.format(self.id))

    def addChannel(self, channel):
        self.channels.append(Channel(self.server, channel))


#####################
# The channel class #
#####################
class Channel:
    def __init__(self, server, channel):
        self.sID = server.id
        self.id = channel.id
        self.slow = False
        self.slowTime = 0
        self.canPromoteYT = True
        self.canPromoteDiscord = True
        self.canChatBot = True
        self.checkRank = True
        self.earnXP = True
        print('Added channel: {}'.format(self.id))
