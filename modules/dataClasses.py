# Currently experimental so may be a bit buggy
# I kinda expect memory leaks as that is very possible
# Luckily only this bot is only on a small number of servers so it is unlikely for a memory leak
# But it is all WiP and will needs improving
import psycopg2 as postG
from config import tokenKeys

host = tokenKeys.dbHost
user = tokenKeys.dbUser
passW = tokenKeys.dbPass

####################
# The server class #
####################
class Server:
    def __init__(self, server):
        self.server = server
        self.id = server.id
        self.channels = []
        self.rolePerms = {}
        self.getRolePerms()
        for channel in server.channels:
            self.addChannel(channel)
        print('Server: {} now initialised'.format(self.id))

    def addChannel(self, channel):
        self.channels.append(Channel(self.server, channel))

    # Need to get the role permissions
    def getRolePerms(self):
        dbName = 'server_{}'.format(self.id)
        conn_string = 'host = {} dbname = {} user = {} password = {}'.format(host, dbName, user, passW)
        conn = postG.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM roleperms')
        result = cursor.fetchall()
        for role in result:
            self.rolePerms[role[1]] = {}
            self.rolePerms[role[1]]['slow'] = role[2]
            self.rolePerms[role[1]]['mute'] = role[3]
            self.rolePerms[role[1]]['banword'] = role[4]
            self.rolePerms[role[1]]['timeout'] = role[5]
            self.rolePerms[role[1]]['clear'] = role[6]
            self.rolePerms[role[1]]['addquote'] = role[7]
            self.rolePerms[role[1]]['editquote'] = role[8]
            self.rolePerms[role[1]]['delquote'] = role[9]
            print(self.rolePerms[role[1]])
        print(self.rolePerms)


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
