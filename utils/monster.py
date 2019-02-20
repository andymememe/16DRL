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
        return "the repr" # TODO: Modify Return
        
    def __str__(self):
        return "the str" # TODO: Modify Return
    
    def _gen_mon(self):
        self.sym = random.choice(SYMSET)
        if self.level > 6:
            self.sym = self.sym.upper()
        self.atk = random.randint(1, self.level * 5)
        self.dfn = random.randint(1, self.level * 5)
        self.hp = random.randint(10, self.level * 100)