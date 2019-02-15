import persistent
import datetime

class Player(persistent.Persistent):
    def __init__(self, playerName, hashID=None):
        self.x = 0
        self.y = 0
        self.playerName = playerName

        # Hash ID
        if hashID is None:
            self.hashID = hash(playerName + str(datetime.datetime.now()))
        else:
            self.hashID = hashID
    
    def setStartPoint(self, x, y):
        self.x = x
        self.y = y