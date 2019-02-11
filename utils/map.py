from enum import Enum
import random

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Map:
    def __init__(self, w, h, roomProb=25, wallPort=15):
        self.map = [['?' for i in range(w)] for j in range(h)]
        self.w = w
        self.h = h
        self.rp = roomProb
        self.wp = wallPort
    
    def mapGenerator(self, level):
        x = self.w // 2
        y = self.h // 2
        
        self._initRoomGenerator(x, y)
        # TODO: Objects
        # TODO: Monsters
    
    def _initRoomGenerator(self, x, y):
        if x > 1 and x < self.w - 2 and y > 1 and y < self.h - 2:
            # Room Interior
            size = random.choice([3, 5, 7])
            half_size = (size - 1) // 2
            for i in range(max(x - half_size, 1),
                           min(x + half_size + 1, self.w - 1)):
                for j in range(max(y - half_size, 1),
                               min(y + half_size + 1, self.h - 1)):
                    self.map[j][i] = 'R'
            
            # Wall
            xRange = list(range(max(x - half_size, 1),
                                min(x + half_size + 1, self.w - 1)))
            yRange = list(range(max(y - half_size, 1),
                                min(y + half_size + 1, self.h - 1)))
            for xi in xRange:
                self.map[max(y - half_size - 1, 0)][xi] = '#'
                self.map[min(y + half_size + 1, self.h - 1)][xi] = '#'
            for yi in yRange:
                self.map[yi][max(x - half_size - 1, 0)] = '#'
                self.map[yi][min(x + half_size + 1, self.w - 1)] = '#'
                
            ## Corner
            self.map[
                max(y - half_size - 1, 0)
            ][
                max(x - half_size - 1, 0)
            ] = '#'
            self.map[
                max(y - half_size - 1, 0)
            ][
                min(x + half_size + 1, self.w - 1)
            ] = '#'
            self.map[
                min(y + half_size + 1,self.h - 1)
            ][
                max(x - half_size - 1, 0)
            ] = '#'
            self.map[
                min(y + half_size + 1, self.h - 1)
            ][
                min(x + half_size + 1, self.w - 1)
            ] = '#'
            
            # Start Point
            self.map[y][x] = '@'
            
            
            # Door & Connection
            ## Up
            if (y - half_size - 1) > 0:
                randomX = random.choice(xRange)
                self.map[y - half_size - 1][randomX] = '+'
                self._corrGenerator(randomX, y - half_size - 2)
            
            ## Down
            if (y + half_size + 1) < (self.h - 1):
                randomX = random.choice(xRange)
                self.map[y + half_size + 1][randomX] = '+'
                self._corrGenerator(randomX, y + half_size + 2)
            
            ## Left
            if (x - half_size - 1) > 0:
                randomY = random.choice(yRange)
                self.map[randomY][x - half_size - 1] = '+'
                self._corrGenerator(x - half_size - 2, randomY)
            
            ## Right
            if (x + half_size + 1) < (self.w - 1):
                randomY = random.choice(yRange)
                self.map[randomY][x + half_size + 1] = '+'
                self._corrGenerator(x + half_size + 2, randomY)
        else:
            raise ValueError('The start point is too close to the bound.')
    
    def _roomGenerator(self, x, y, formalDir):
        dir, lb, ub = self._roomInfoGenerator(x, y, formalDir)
        # TODO: Make Room
    
    def _roomInfoGenerator(self, x, y, formalDir):
        infoList = []
        for cDir in [Direction.UP, Direction.DOWN]:
            check = y > 3 if cDir == Direction.UP else y < self.h - 4
            if check and not formalDir == cDir:
                ok = True
                ylb = y - 4 if cDir == Direction.UP else y
                yub = y + 1 if cDir == Direction.UP else y + 5
                for cy in range(ylb, yub):
                    if map[cy][x] == 'R':
                        ok = False
                        break
                if ok:
                    lb = max(x - 7, 0)
                    ub = min(x + 7, self.w - 1)
                    for cx in range(lb, x):
                        for cy in range(ylb, yub):
                            if map[cy][cx] == 'R':
                                lb = cx + 1                
                    for cx in range(ub, x, -1):
                        for cy in range(ylb, yub):
                            if map[cy][cx] == 'R':
                                ub = cx - 1
                    if (ub - lb + 1) > 4:
                        infoList.append((cDir, lb, ub))
        for cDir in [Direction.LEFT, Direction.RIGHT]:
            check = x > 3 if cDir == Direction.LEFT else x < self.w - 4
            if check and not formalDir == cDir:
                ok = True
                xlb = x - 4 if cDir == Direction.LEFT else x
                xub = x + 1 if cDir == Direction.LEFT else x + 5
                for cx in range(xlb, xub):
                    if map[y][cx] == 'R':
                        ok = False
                        break
                if ok:
                    lb = max(y - 7, 0)
                    ub = min(y + 7, self.h - 1)
                    for cy in range(lb, y):
                        for cx in range(xlb, xub):
                            if map[cy][cx] == 'R':
                                lb = cy + 1                
                    for cy in range(ub, y, -1):
                        for cx in range(xlb, xub):
                            if map[cy][cx] == 'R':
                                ub = cy - 1
                    if (ub - lb + 1) > 4:
                        infoList.append((cDir, lb, ub))
        return random.choice(infoList)
    
    def _corrGenerator(self, x, y):
        self.map[y][x] = '.'
        # TODO: Make Corridor
    
    def _corrInfoRandom(self, x, y):
        # TODO: Get Corridor Info
        pass
    
if __name__ == '__main__':
    map = Map(80, 60)
    map.mapGenerator(1)
    with open('test.debug', 'w') as f:
        for yi in map.map:
            for xi in yi:
                f.write(xi)
            f.write('\n')