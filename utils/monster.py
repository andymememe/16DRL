class Monster():
    def __init__(self, x, y, level):
        self.x = x
        self.y = y
        self.level = level
        self.atk = 0
        self.dfn = 0
        self.hp = 0
        
        self._gen_mon()
    
    def _gen_mon(self):
        self.sym = None
        self.atk = 0
        self.dfn = 0
        self.hp = 0