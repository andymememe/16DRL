import datetime

class Player():
    def __init__(self, playerName, hashID=None):
        # Coordination
        self.x = 0
        self.y = 0
        
        # Data
        self.level = 1
        self.score = 0
        self.hp = 100
        self.atk = 0
        self.dfn = 0
        self.inventory = []
        self.equipped = []

        # ID
        self.playerName = playerName
        self.finished = False
        if hashID is None:
            self.hashID = hash(playerName + str(datetime.datetime.now()))
        else:
            self.hashID = hashID
    
    def __repr__(self):
        return "the repr" # TODO: Modify Return
        
    def __str__(self):
        return "the str" # TODO: Modify Return
    
    def setStartPoint(self, x, y):
        self.x = x
        self.y = y
    
    def addInventory(self, obj):
        if obj.usage == 0:
            self.score += obj.attr['score']
            return
        else:
            self.inventory.append(obj)