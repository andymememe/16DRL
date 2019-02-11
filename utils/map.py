from enum import Enum
import random

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Map:
    def __init__(self, w, h, roomProb=25, wallPort=15):
        self.map = [['#' for i in range(w)] for j in range(h)]
        self.w = w
        self.h = h
        self.rp = roomProb
        self.wp = wallPort
    
    def 
    
    def mapGenerator(self, level):
        x = self.w // 2
        y = self.h // 2
    
    def _roomGenerator(self, x, y, dir):
        if dir == Direction.UP or dir == Direction.DOWN:
            pass
        elif dir == DIrection.LEFT or dir == Direction.RIGHT:
            pass
    
    def _roomDirCheck(self, x, y, dir):
        dir = []
        for cDir in [Direction.UP, Direction.DOWN]:
            check = y > 3 if cDir == Direction.UP else y < self.h - 4
            if check and not dir == cDir:
                ok = True
                ylb = y - 4 if cDir == Direction.UP else y
                yrb = y + 1 if cDir == Direction.UP else y + 5
                for cy in range(ylb, yrb):
                    if map[cy][x] == 'R':
                        ok = False
                        break
                if ok:
                    lb = max(x - 7, 0)
                    rb = min(x + 7, self.w - 1)
                    for cx in range(lb, x):
                        for cy in range(ylb, yrb):
                            if map[cy][cx] == 'R':
                                lb = cx + 1                
                    for cx in range(rb, x, -1):
                        for cy in range(ylb, yrb):
                            if map[cy][cx] == 'R':
                                rb = cx - 1
                    if (rb - lb + 1) > 4:
                        dir.append((cDir, lb, rb))
        for cDir in [Direction.LEFT, Direction.RIGHT]:
            check = x > 3 if cDir == Direction.LEFT else x < self.w - 4
            if check and not dir == cDir:
                ok = True
                xlb = x - 4 if cDir == Direction.LEFT else x
                xrb = x + 1 if cDir == Direction.LEFT else x + 5
                for cx in range(xlb, xrb):
                    if map[y][cx] == 'R':
                        ok = False
                        break
                if ok:
                    lb = max(y - 7, 0)
                    rb = min(y + 7, self.h - 1)
                    for cy in range(lb, y):
                        for cx in range(xlb, xrb):
                            if map[cy][cx] == 'R':
                                lb = cy + 1                
                    for cy in range(rb, y, -1):
                        for cx in range(xlb, xrb):
                            if map[cy][cx] == 'R':
                                rb = cy - 1
                    if (rb - lb + 1) > 4:
                        dir.append((cDir, lb, rb))
        return random.choice(dir)
    
    def _corrGenerator(self, x, y):
        pass
    
    def _corrDirRandom(self, x, y):
        pass
    
    def _corrLengthRandom(self, x, y, dir):
        pass