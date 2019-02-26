import datetime, random

class Player():
    def __init__(self, playerName, hashID=None):
        # Coordination
        self.x = 0
        self.y = 0
        
        # Data
        self.level = 1
        self.score = 0
        self.max_hp = 100
        self.hp = 100
        self.atk = 6
        self.dfn = 6
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
            self.hashID = '16DRL_' + \
                          str(hash(playerName + str(datetime.datetime.now())))
        else:
            self.hashID = '16DRL_' + hashID
    
    def __repr__(self):
        return "lv.{0} => hp: {1}, atk: {2}, dfn: {3}".format(self.level,
                                                              self.hp,
                                                              self.atk,
                                                              self.dfn)
        
    def __str__(self):
        return "lv.{0}".format(self.level)
    
    def getInventory(self):
        return list(self.inventory)
    
    def getWearable(self):
        return [i if i.usage == 1 else None for i in self.inventory]
    
    def getUsable(self):
        return [i if i.usage == 2 else None for i in self.inventory]
    
    def setStartPoint(self, x, y):
        self.x = x
        self.y = y
    
    def setHit(self, hit):
        self.hp = max(0, self.hp - hit)
        self.finished = self.hp <= 0
    
    def setInventory(self, obj):
        if obj.usage == 0:
            self.score += obj.attrs['score']
        else:
            self.inventory.append(obj)
    
    def setLevel(self, level):
        self.level = level
    
    def getDfn(self):
        return self.dfn * self.dfn_mul
        
    def getAtk(self):
        return self.atk * self.atk_mul
    
    def move(self, x, y):
        self.x = x
        self.y = y
    
    def combat(self, hit):
        if random.randint(1, 100) < min(75, 25 + (self.level - 1) * 4.2):
            self.setHit(max(0, hit - self.getDfn()))
            return True, max(0, hit - self.getDfn())
        return False, 0
    
    def wear(self, index, map):
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
                elif k == 'max_hp':
                    self.max_hp -= temp.attrs[k]
                elif k == 'atk_mul':
                    self.atk_mul -= obj.attrs[k]
                elif k == 'dfn_mul':
                    self.dfn_mul -= obj.attrs[k]
            self.inventory.append(temp)
        for k in obj.attrs:
            if k == 'atk':
                self.atk += obj.attrs[k]
            elif k == 'dfn':
                self.dfn += obj.attrs[k]
            elif k == 'max_hp':
                self.max_hp += obj.attrs[k]
            elif k == 'atk_mul':
                self.atk_mul += obj.attrs[k]
            elif k == 'dfn_mul':
                self.dfn_mul += obj.attrs[k]
        self.equipped[slot] = obj
        self.inventory.remove(obj)
        map.logs.append('{0} wore a(n) {1}.'.format(self.playerName,
                                                    obj.obj_type))
    
    def use(self, index, map):
        obj = self.inventory[index]
        for k in obj.attrs:
            if k == 'atk':
                self.atk += obj.attrs[k]
            elif k == 'dfn':
                self.dfn += obj.attrs[k]
            elif k == 'hp':
                self.heal(obj.attrs[k])
            elif k == 'max_hp':
                self.max_hp += obj.attrs[k]
        self.inventory.remove(obj)
        map.logs.append('{0} used a(n) {1}.'.format(self.playerName,
                                                    obj.obj_type))
    
    def heal(self, heal_hp):
        self.hp = min(self.max_hp, self.hp + heal_hp)
    
    def victory(self):
        self.finished = True