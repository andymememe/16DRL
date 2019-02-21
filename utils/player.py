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
        return "lv.{0} => hp: {1}, atk: {2}, dfn: {3}".format(self.level,
                                                              self.hp,
                                                              self.atk,
                                                              self.dfn)
        
    def __str__(self):
        return "lv.{0}".format(self.level)
    
    def setStartPoint(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, x, y):
        self.x = x
        self.y = y
    
    def combat(self, hit):
        self.hp = max(0, self.hp - hit)
        self.finished = True
    
    def addInventory(self, obj):
        if obj.usage == 0:
            self.score += obj.attr['score']
        else:
            self.inventory.append(obj)
    
    def wear(self, index):
        pass
    
    def use(self, index):
        pass