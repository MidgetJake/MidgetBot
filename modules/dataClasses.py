# This is all just experimental and won't be worked on too much currently

class User:
    def __init__(self, user):
        self.user = user
        self.id = user.id
        self.messagesSent = 0
        self.level = 1
        self.xp = 0
        self.totalXp = 0

    def addXp(self, change):
        self.xp += change
        self.totalXp += change

    def checkLevel(self):
        if self.xp > (self.level*100):
            self.level += 1
            self.xp = 0

class Server:
    def __init__(self, server):
        self.server = server
        self.id = server.id
        self.members = []

    def addMember(self, user):
        self.members.append(User(user))
