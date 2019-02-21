import random

SYMSET = [chr(i) for i in range(ord('a'), ord('z') + 1)]

class Monster():
    def __init__(self, x, y, level):
        self.x = x
        self.y = y
        self.level = max(level, 1)
        self.atk = 0
        self.dfn = 0
        self.hp = 0
        
        self._gen_mon()
    
    def __repr__(self):
        return "{0} => hp: {1}, atk: {2}, dfn: {3}".format(self.sym,
                                                           self.hp,
                                                           self.atk,
                                                           self.dfn)
        
    def __str__(self):
        return self.sym
    
    def _gen_mon(self):
        self.sym = random.choice(SYMSET)
        if self.level > 6:
            self.sym = self.sym.upper()
        self.atk = random.randint(1, self.level * 5)
        self.dfn = random.randint(1, self.level * 5)
        self.hp = random.randint(10, self.level * 100)
    
    def move(self, x, y):
        self.x = x
        self.y = y
    
    def combat(self, hit):
        if random.randint(1, 100) > min(75, 25 + (self.level - 1) * 4.2) or \
           (hit - self.dfn) > 50:
            self.hp = max(0, self.hp - max(0, hit - self.dfn))