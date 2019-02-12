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
                self._corrGenerator(randomX, y - half_size - 2, Direction.UP)
            
            ## Down
            if (y + half_size + 1) < (self.h - 1):
                randomX = random.choice(xRange)
                self.map[y + half_size + 1][randomX] = '+'
                self._corrGenerator(randomX, y + half_size + 2, Direction.DOWN)
            
            ## Left
            if (x - half_size - 1) > 0:
                randomY = random.choice(yRange)
                self.map[randomY][x - half_size - 1] = '+'
                self._corrGenerator(x - half_size - 2, randomY, Direction.LEFT)
            
            ## Right
            if (x + half_size + 1) < (self.w - 1):
                randomY = random.choice(yRange)
                self.map[randomY][x + half_size + 1] = '+'
                self._corrGenerator(x + half_size + 2, randomY, Direction.RIGHT)
        else:
            raise ValueError('The start point is too close to the bound.')
    
    def _roomGenerator(self, x, y, formalDir):
        dir, lb, ub = self._roomInfoGenerator(x, y, formalDir)
        if dir == None:
            return False
        rLB = random.randint(lb, ub - 4)
        rUB = random.randint(rLB + 4, ub)
        
        # Vertical
        if dir == Direction.UP and Direction.DOWN:
            step = -1 if dir == Direction.UP else 1
        # Horizon
        elif dir == Direction.LEFT and Direction.RIGHT:
            step = -1 if dir == Direction.LEFT else 1
        return True
    
    def _roomInfoGenerator(self, x, y, formalDir):
        infoList = []
        for cDir in [Direction.UP, Direction.DOWN]:
            check = y > 3 if cDir == Direction.UP else y < self.h - 4
            if formalDir == Direction.UP:
                bDir = Direction.DOWN
            else:
                bDir = Direction.UP
            
            if check and not bDir == cDir:
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
            if formalDir == Direction.LEFT:
                bDir = Direction.RIGHT
            else:
                bDir = Direction.LEFT
            
            if check and not bDir == cDir:
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
        if len(infoList) > 0:
            return random.choice(infoList)
        return None, None, None
    
    def _corrGenerator(self, x, y, formalDir):
        dir, length = self._corrInfoRandom(x, y, formalDir)
        if dir == None:
            return
        length = random.randint(3, length)
        nx = x
        ny = y
        
        if dir == Direction.UP:
            for i in range(length):
                self.map[y - i][x] = '.'
            ny = y - length
        elif dir == Direction.DOWN:
            for i in range(length):
                self.map[y + i][x] = '.'
            ny = y + length
        elif dir == Direction.LEFT:
            for i in range(length):
                self.map[y][x - i] = '.'
            nx = x - length
        elif dir == Direction.RIGHT:
            for i in range(length):
                self.map[y][x + i] = '.'
            nx = x + length
        
        if nx < 1 or nx > self.w - 2 or \
           ny < 1 or ny > self.h - 2:
            return
        
        self._corrGenerator(nx, ny, dir)
            
    def _corrInfoRandom(self, x, y, formalDir):
        info = []
        if not formalDir == Direction.DOWN:
            cy = y - 1
            for cy in range(y - 1, max(y - 7, 0), -1):
                if self.map[cy][x] not in ['?', '.']:
                    break
            if y - cy > 3:
                info.append((Direction.UP, y - cy))
        if not formalDir == Direction.UP:
            cy = y + 1
            for cy in range(y + 1, min(y + 7, self.h - 1)):
                if self.map[cy][x] not in ['?', '.']:
                    break
            if cy - y > 3:
                info.append((Direction.DOWN, cy - y))
        if not formalDir == Direction.LEFT:
            cx = x + 1
            for cx in range(x + 1, min(x + 7, self.w - 1)):
                if self.map[y][cx] not in ['?', '.']:
                    break
            if cx - x > 3:
                info.append((Direction.RIGHT, cx - x))
        if not formalDir == Direction.RIGHT:
            cx = x - 1
            for cx in range(x - 1, max(x - 7, 0), -1):
                if self.map[y][cx] not in ['?', '.']:
                    break
            if x - cx > 3:
                info.append((Direction.LEFT, x - cx))
        if len(info) > 1:
            return random.choice(info)
        return None, None
    
if __name__ == '__main__':
    map = Map(80, 60)
    map.mapGenerator(1)
    with open('test.debug', 'w') as f:
        for yi in map.map:
            for xi in yi:
                f.write(xi)
            f.write('\n')