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
        self.atk = 6
        self.dfn = 6
        self.hp_mul = 1
        self.atk_mul = 1
        self.dfn_mul = 1
        self.inventory = []
        self.equipped = {
            'right-hand': None,
            'left-hand': None,
            'right-ring': None,
            'left-ring': None,
            'amulet': None
        }

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
        if random.randint(1, 100) < min(75, 25 + (self.level - 1) * 4.2):
            self.hp = max(0, self.hp - hit)
            self.finished = self.hp <= 0
    
    def addInventory(self, obj):
        if obj.usage == 0:
            self.score += obj.attr['score']
        else:
            self.inventory.append(obj)
    
    def wear(self, index):
        obj = self.inventory[index]
        slot = ''
        if obj.obj_type in ['weapon', 'wand']:
            slot = 'right-hand'
        elif obj.obj_type == 'armor':
            slot = 'left-hand'
        elif obj.obj_type == 'ring':
            if self.equipped['left-ring'] is None:
                slot = 'left-ring'
            else:
                slot = 'right-ring'
        elif obj.obj_type == 'amulet':
            slot = 'amulet'
        
        if self.equipped[slot] is not None:
            temp = self.equipped[slot]
            for k in temp.attrs:
                if k == 'atk':
                    self.atk -= temp.attrs[k]
                elif k == 'dfn':
                    self.dfn -= temp.attrs[k]
                elif k == 'hp:'
                    self.hp -= temp.attrs[k]
                elif k == 'atk_mul':
                    self.atk_mul -= obj.attrs[k]
                elif k == 'dfn_mul':
                    self.dfn_mul -= obj.attrs[k]
                elif k == 'hp_mul:'
                    self.hp_mul -= obj.attrs[k]
            self.inventory.append(temp)
        for k in obj.attrs:
            if k == 'atk':
                self.atk += obj.attrs[k]
            elif k == 'dfn':
                self.dfn += obj.attrs[k]
            elif k == 'hp':
                self.hp += obj.attrs[k]
            elif k == 'atk_mul':
                self.atk_mul += obj.attrs[k]
            elif k == 'dfn_mul':
                self.dfn_mul += obj.attrs[k]
            elif k == 'hp_mul:'
                self.hp_mul += obj.attrs[k]
        self.equipped[slot] = obj
    
    def use(self, index):
        obj = self.inventory[index]
        for k in obj.attrs:
            if k == 'atk':
                self.atk += obj.attrs[k]
            elif k == 'dfn':
                self.dfn += obj.attrs[k]
            elif k == 'hp':
                self.hp += obj.attrs[k]
        self.inventory.remove(obj)