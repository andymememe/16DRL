import persistent

class Monster(persistent.Persistent):
    def __init__(self, x, y, sym):
        self.x = x
        self.y = y
        self.sym = sym