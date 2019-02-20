import datetime

class Player():
    def __init__(self, playerName, hashID=None):
        # Coordination
        self.x = 0
        self.y = 0
        
        # Data
        self.level = 1
        self.hp = 100
        self.score = 0

        # ID
        self.playerName = playerName
        self.finished = False
        if hashID is None:
            self.hashID = hash(playerName + str(datetime.datetime.now()))
        else:
            self.hashID = hashID
    
    def setStartPoint(self, x, y):
        self.x = x
        self.y = y