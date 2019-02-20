# map.py, a simple python dungeon generator by
# James Spencer <jamessp [at] gmail.com>.

# To the extent possible under law, the person who associated CC0 with
# pathfinder.py has waived all copyright and related or neighboring rights
# to pathfinder.py.

# You should have received a copy of the CC0 legalcode along with this
# work. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
import random
from utils.monster import Monster
from utils.object import Object

CHARACTER_TILES = {# Map Objects
                   'stone': ' ',
                   'floor': '.',
                   'wall' : '#',
                   'door' : '+',
                   # Acuirable Objects
                   'money': '$',
                   'weapon': ')',
                   'armor': '[',
                   'edible': '%',
                   'scroll': '?',
                   'wand': '/',
                   'ring': '=',
                   'potion': '!',
                   'key_item': '(',
                   'amulet': '"',
                   # Obstacle Objects
                   'altar': '_',
                   'statue': "'",
                   'obstacle': '0',
                   'fountain': '{',
                   # Passing Objects
                   'palyer': '@',
                   'trap': '.',
                   'monster': '.',
                   'detected_trap': '^',
                   'down_stair': '>',
                   'throne': '\\'}

class Map():
    def __init__(self, level, lastLevel=False, width=70, height=60,
                 max_rooms=15, max_objs_in_room=30, max_traps=30, max_mons=20,
                 min_room_xy=5, max_room_xy=10,
                 rooms_overlap=False, random_connections=1,
                 random_spurs=3, tiles=CHARACTER_TILES):
        self.level = level
        self.lastLevel = lastLevel
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.max_objs_in_room = max_objs_in_room
        self.max_traps = max_traps
        self.max_mons = max_mons
        self.min_room_xy = min_room_xy
        self.max_room_xy = max_room_xy
        self.rooms_overlap = rooms_overlap
        self.random_connections = random_connections
        self.random_spurs = random_spurs
        self.tiles = CHARACTER_TILES
        self.level = []
        self.room_list = []
        self.corridor_list = []
        self.door_list = []
        self.objs_list = []
        self.traps_list = []
        self.mons_list = []
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)
        self.tiles_level = []
 
    def gen_room(self):
        x, y, w, h = 0, 0, 0, 0
 
        w = random.randint(self.min_room_xy, self.max_room_xy)
        h = random.randint(self.min_room_xy, self.max_room_xy)
        x = random.randint(1, (self.width - w - 1))
        y = random.randint(1, (self.height - h - 1))
 
        return [x, y, w, h]
 
    def room_overlapping(self, room, room_list):
        x = room[0]
        y = room[1]
        w = room[2]
        h = room[3]
 
        for current_room in room_list:
 
            # The rectangles don't overlap if
            # one rectangle's minimum in some dimension
            # is greater than the other's maximum in
            # that dimension.
 
            if (x < (current_room[0] + current_room[2]) and
                current_room[0] < (x + w) and
                y < (current_room[1] + current_room[3]) and
                current_room[1] < (y + h)):
 
                return True
 
        return False
  
    def corridor_between_points(self, x1, y1, x2, y2, join_type='either'):
        if x1 == x2 and y1 == y2 or x1 == x2 or y1 == y2:
            return [(x1, y1), (x2, y2)]
        else:
            # 2 Corridors
            # NOTE: Never randomly choose a join that will go out of bounds
            # when the walls are added.
            join = None
            if join_type is 'either' and set([0, 1]).intersection(
                 set([x1, x2, y1, y2])):
 
                join = 'bottom'
            elif join_type is 'either' and set([self.width - 1,
                 self.width - 2]).intersection(set([x1, x2])) or set(
                 [self.height - 1, self.height - 2]).intersection(
                 set([y1, y2])):
 
                join = 'top'
            elif join_type is 'either':
                join = random.choice(['top', 'bottom'])
            else:
                join = join_type
 
            if join is 'top':
                return [(x1, y1), (x1, y2), (x2, y2)]
            elif join is 'bottom':
                return [(x1, y1), (x2, y1), (x2, y2)]
 
    def join_rooms(self, room_1, room_2, join_type='either'):
        # sort by the value of x
        sorted_room = [room_1, room_2]
        sorted_room.sort(key=lambda x_y: x_y[0])
 
        x1 = sorted_room[0][0]
        y1 = sorted_room[0][1]
        w1 = sorted_room[0][2]
        h1 = sorted_room[0][3]
        x1_2 = x1 + w1 - 1
        y1_2 = y1 + h1 - 1
 
        x2 = sorted_room[1][0]
        y2 = sorted_room[1][1]
        w2 = sorted_room[1][2]
        h2 = sorted_room[1][3]
        x2_2 = x2 + w2 - 1
        y2_2 = y2 + h2 - 1
 
        # overlapping on x
        if x1 < (x2 + w2) and x2 < (x1 + w1):
            jx1 = random.randint(x2, x1_2)
            jx2 = jx1
            tmp_y = [y1, y2, y1_2, y2_2]
            tmp_y.sort()
            jy1 = tmp_y[1] + 1
            jy2 = tmp_y[2] - 1
            
            self.door_list.append((jx1, jy1))
            self.door_list.append((jx2, jy2))
            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)
 
        # overlapping on y
        elif y1 < (y2 + h2) and y2 < (y1 + h1):
            if y2 > y1:
                jy1 = random.randint(y2, y1_2)
                jy2 = jy1
            else:
                jy1 = random.randint(y1, y2_2)
                jy2 = jy1
            tmp_x = [x1, x2, x1_2, x2_2]
            tmp_x.sort()
            jx1 = tmp_x[1] + 1
            jx2 = tmp_x[2] - 1
 
            self.door_list.append((jx1, jy1))
            self.door_list.append((jx2, jy2))
            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)
 
        # no overlap
        else:
            join = None
            if join_type is 'either':
                join = random.choice(['top', 'bottom'])
            else:
                join = join_type
 
            if join is 'top':
                if y2 > y1:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2 - 1
                    
                    self.door_list.append((jx1, jy1))
                    self.door_list.append((jx2, jy2))
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'bottom')
                    self.corridor_list.append(corridors)
                else:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1 - 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    
                    self.door_list.append((jx1, jy1))
                    self.door_list.append((jx2, jy2))
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'top')
                    self.corridor_list.append(corridors)
 
            elif join is 'bottom':
                if y2 > y1:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1_2 + 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
            
                    self.door_list.append((jx1, jy1))
                    self.door_list.append((jx2, jy2))
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'top')
                    self.corridor_list.append(corridors)
                else:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2_2 + 1
                    
                    self.door_list.append((jx1, jy1))
                    self.door_list.append((jx2, jy2))
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'bottom')
                    self.corridor_list.append(corridors)

    def gen_objs_in_room(self, position):
        x, y = position
        self.objs_list.append(Object(x, y, self.level))
        self.level[y][x] = self.obj_type

    def gen_traps(self, position):
        x, y = position
        self.traps_list.append((x, y, 0))
        self.level[y][x] = 'trap'
    
    def gen_monsters(self, position):
        x, y = position
        self.mons_list.append(Monster(x, y, self.level))
        self.level[y][x] = 'monster'

    def gen_start_end(self, positionS, positionE):
        self.start_pos = positionS
        self.end_pos = positionE
        sx, sy = self.start_pos
        ex, ey = self.end_pos
        if self.lastLevel:
            self.level[ey][ex] = 'throne'
        else:
            self.level[ey][ex] = 'down_stair'
  
    def gen_level(self):
        # build an empty dungeon, blank the room and corridor lists
        for i in range(self.height):
            self.level.append(['stone'] * self.width)
        self.room_list = []
        self.corridor_list = []
        self.door_list = []
        self.objs_list = []
        self.mons_list = []
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)
 
        max_iters = self.max_rooms * 5
 
        # create room
        for a in range(max_iters):
            tmp_room = self.gen_room()
 
            if self.rooms_overlap or not self.room_list:
                self.room_list.append(tmp_room)
            else:
                tmp_room = self.gen_room()
                tmp_room_list = self.room_list[:]
 
                if self.room_overlapping(tmp_room, tmp_room_list) is False:
                    self.room_list.append(tmp_room)
 
            if len(self.room_list) >= self.max_rooms:
                break
 
        # connect the rooms
        for a in range(len(self.room_list) - 1):
            self.join_rooms(self.room_list[a], self.room_list[a + 1])
 
        # do the random joins
        for a in range(self.random_connections):
            room_1 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)
 
        # do the spurs
        for a in range(self.random_spurs):
            room_1 = [random.randint(2, self.width - 2), random.randint(
                     2, self.height - 2), 1, 1]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)
 
        # fill the map
        # paint rooms
        for room_num, room in enumerate(self.room_list):
            for b in range(room[2]):
                for c in range(room[3]):
                    self.level[room[1] + c][room[0] + b] = 'floor'
 
        # paint corridors
        for corridor in self.corridor_list:
            x1, y1 = corridor[0]
            x2, y2 = corridor[1]
            for width in range(abs(x1 - x2) + 1):
                for height in range(abs(y1 - y2) + 1):
                    self.level[min(y1, y2) + height][
                        min(x1, x2) + width] = 'floor'
 
            if len(corridor) == 3:
                x3, y3 = corridor[2]
 
                for width in range(abs(x2 - x3) + 1):
                    for height in range(abs(y2 - y3) + 1):
                        self.level[min(y2, y3) + height][
                            min(x2, x3) + width] = 'floor'
 
        # paint the walls
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                if self.level[row][col] == 'floor':
                    if self.level[row - 1][col - 1] == 'stone':
                        self.level[row - 1][col - 1] = 'wall'
 
                    if self.level[row - 1][col] == 'stone':
                        self.level[row - 1][col] = 'wall'
 
                    if self.level[row - 1][col + 1] == 'stone':
                        self.level[row - 1][col + 1] = 'wall'
 
                    if self.level[row][col - 1] == 'stone':
                        self.level[row][col - 1] = 'wall'
 
                    if self.level[row][col + 1] == 'stone':
                        self.level[row][col + 1] = 'wall'
 
                    if self.level[row + 1][col - 1] == 'stone':
                        self.level[row + 1][col - 1] = 'wall'
 
                    if self.level[row + 1][col] == 'stone':
                        self.level[row + 1][col] = 'wall'
 
                    if self.level[row + 1][col + 1] == 'stone':
                        self.level[row + 1][col + 1] = 'wall'
 
        # paint doors
        for door in self.door_list:
            x, y = door
            if (self.level[y - 1][x] == 'wall' and \
                self.level[y + 1][x] == 'wall' and \
                self.level[y][x - 1] == 'floor' and \
                self.level[y][x + 1] == 'floor') or \
               (self.level[y - 1][x] == 'floor' and \
                self.level[y + 1][x] == 'floor' and \
                self.level[y][x - 1] == 'wall' and \
                self.level[y][x + 1] == 'wall'):
                self.level[y][x] = 'door'
        
        # insert objects in map
        # insert objs in room
        for a in range(self.max_objs_in_room):
            room = random.choice(self.room_list[1:-1])
            ox, oy = (random.randint(room[0], room[0] + room[2] - 1),
                      random.randint(room[1], room[1] + room[3] - 1))
            while not self.level[oy][ox] == 'floor' and not self.check_path(ox, oy):
                room = random.choice(self.room_list[1:-1])
                ox, oy = (random.randint(room[0], room[0] + room[2] - 1),
                          random.randint(room[1], room[1] + room[3] - 1))
            self.gen_objs_in_room((ox, oy))

        # insert traps
        for a in range(self.max_traps):
            place_type = random.choice(["corr, room"])
            tx = 0
            ty = 0
            if place_type == "corr":
                corr = random.choice(self.corridor_list)
                end_index = random.randint(1, len(corr) - 1)
                tx, ty = (random.randint(corr[end_index - 1][0], corr[end_index][0]),
                          random.randint(corr[end_index - 1][1], corr[end_index][1]))
                while not self.level[ty][tx] == 'floor':
                    corr = random.choice(self.corridor_list)
                    end_index = random.randint(1, len(corr) - 1)
                    tx, ty = (random.randint(corr[end_index - 1][0], corr[end_index][0]),
                              random.randint(corr[end_index - 1][1], corr[end_index][1]))
            else:
                room = random.choice(self.room_list[1:-1])
                tx, ty = (random.randint(room[0], room[0] + room[2] - 1),
                          random.randint(room[1], room[1] + room[3] - 1))
                while not self.level[ty][tx] == 'floor':
                    room = random.choice(self.room_list[1:-1])
                    tx, ty = (random.randint(room[0], room[0] + room[2] - 1),
                              random.randint(room[1], room[1] + room[3] - 1))
            self.gen_traps((tx, ty))

        # insert monsters
        for a in range(self.max_mons):
            place_type = random.choice(["corr, room"])
            mx = 0
            my = 0
            if place_type == "corr":
                corr = random.choice(self.corridor_list)
                end_index = random.randint(1, len(corr) - 1)
                mx, my = (random.randint(corr[end_index - 1][0], corr[end_index][0]),
                          random.randint(corr[end_index - 1][1], corr[end_index][1]))
                while not self.level[my][mx] == 'floor':
                    corr = random.choice(self.corridor_list)
                    end_index = random.randint(1, len(corr) - 1)
                    mx, my = (random.randint(corr[end_index - 1][0], corr[end_index][0]),
                              random.randint(corr[end_index - 1][1], corr[end_index][1]))
            else:
                room = random.choice(self.room_list[1:-1])
                mx, my = (random.randint(room[0], room[0] + room[2] - 1),
                          random.randint(room[1], room[1] + room[3] - 1))
                while not self.level[my][mx] == 'floor':
                    room = random.choice(self.room_list[1:-1])
                    mx, my = (random.randint(room[0], room[0] + room[2] - 1),
                              random.randint(room[1], room[1] + room[3] - 1))
            self.gen_monsters((mx, my))
        
        # Start & End
        # Start
        room = self.room_list[0]
        sx, sy = (random.randint(room[0], room[0] + room[2] - 1),
                  random.randint(room[1], room[1] + room[3] - 1))
        while not self.level[sy][sx] == 'floor':
            sx, sy = (random.randint(room[0], room[0] + room[2] - 1),
                      random.randint(room[1], room[1] + room[3] - 1))
        # End
        room = self.room_list[-1]
        ex, ey = (random.randint(room[0], room[0] + room[2] - 1),
                  random.randint(room[1], room[1] + room[3] - 1))
        while not self.level[ey][ex] == 'floor':
            ex, ey = (random.randint(room[0], room[0] + room[2] - 1),
                      random.randint(room[1], room[1] + room[3] - 1))
        self.gen_start_end((sx, sy), (ex, ey))
                            
    def gen_tiles_level(self):
        for row_num, row in enumerate(self.level):
            tmp_tiles = []
 
            for col_num, col in enumerate(row):
                tmp_tiles.append(self.tiles[col])
 
            self.tiles_level.append(''.join(tmp_tiles))
    
    def check_path(self, x, y):
        # Check Door
        if self.level[y - 1][x] == 'door' or \
           self.level[y + 1][x] == 'door' or \
           self.level[y][x - 1] == 'door' or \
           self.level[y][x + 1] == 'door':
            return False
        
        # Check Path
        if self.level[y - 1][x - 1] == 'floor' and \
           self.level[y - 1][x] == 'floor' and \
           self.level[y - 1][x + 1] == 'floor':
            return True
        if self.level[y + 1][x - 1] == 'floor' and \
           self.level[y + 1][x] == 'floor' and \
           self.level[y + 1][x + 1] == 'floor':
            return True
        if self.level[y - 1][x - 1] == 'floor' and \
           self.level[y][x - 1] == 'floor' and \
           self.level[y + 1][x - 1] == 'floor':
            return True
        if self.level[y - 1][x + 1] == 'floor' and \
           self.level[y][x + 1] == 'floor' and \
           self.level[y + 1][x + 1] == 'floor':
            return True

        # Check Corner Path
        if self.level[y - 1][x] == 'floor' and \
           self.level[y - 1][x + 1] == 'floor' and \
           self.level[y][x + 1] == 'floor':
            return True
        if self.level[y][x + 1] == 'floor' and \
           self.level[y + 1][x + 1] == 'floor' and \
           self.level[y + 1][x] == 'floor':
            return True
        if self.level[y + 1][x] == 'floor' and \
           self.level[y + 1][x - 1] == 'floor' and \
           self.level[y][x - 1] == 'floor':
            return True
        if self.level[y][x - 1] == 'floor' and \
           self.level[y - 1][x - 1] == 'floor' and \
           self.level[y - 1][x] == 'floor':
            return True
        
        # No Path
        return False


    def set_player(self, player):
        player.setStartPoint(self.start_pos[0], self.start_pos[1])
    
    def update(self, player, command):
        pass
    
    def show_map(self, player):
        cameraX = min(max(4, player.x), self.width - 5)
        cameraY = min(max(4, player.y), self.height - 5)

        level = list(self.tiles_level)
        level[player.y] = level[player.y][:player.x] + '@' + level[player.y][player.x + 1:]
        for mon in self.mons_list:
            if mon.x < cameraX + 5 and mon.y < cameraY + 5:
                level[mon.y] = level[mon.y][:mon.x] + mon.sym + level[mon.y][mon.x + 1:]
        displayMap = [row[cameraX - 4:cameraX + 5] for row in level[cameraY - 4:cameraY + 5]]
        return displayMap
    
    def show_total_map(self, player):
        level = list(self.tiles_level)
        level[player.y] = level[player.y][:player.x] + '@' + level[player.y][player.x + 1:]
        for mon in self.mons_list:
            level[mon.y] = level[mon.y][:mon.x] + mon.sym + level[mon.y][mon.x + 1:]
        return level