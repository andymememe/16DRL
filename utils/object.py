import random

OBJ_LIST = [# Money (usage = 0)
            'money',
            # Wearable (usage = 1)
            'weapon',
            'wand',
            'armor',
            'ring',
            'amulet',
            # Usable (usage = 2)
            'edible',
            'scroll',
            'potion']

class Object():
    def __init__(self, x, y, level, key_item=False):
        self.x = x
        self.y = y
        self.level = level
        self.key_item = key_item
        self.attr = {}
        
        if self.key_item:
            self.obj_type = 'key_item'
        else:
            self._gen_obj()
    
    def __repr__(self):
        return "the repr" # TODO: Modify Return
        
    def __str__(self):
        return "the str" # TODO: Modify Return
    
    def _gen_obj(self):
        self.obj_type = random.choice(OBJ_LIST)
        self.usage = 0
        if self.obj_type == 'money':
            self.attr['score'] = random.randint(10, (self.level ** 2) * 100)
        elif self.obj_type in ['weapon', 'wand']:
            self.usage = 1
            self.attr['atk'] = random.randint(10, 10 + self.level * 15)
        elif self.obj_type == 'armor':
            self.usage = 1
            self.attr['dfn'] = random.randint(10, 10 + self.level * 15)
        elif self.obj_type in ['ring', 'amulet']:
            self.usage = 1
            # TODO: Add attribute for wear it
        elif self.obj_type == 'edible':
            self.usage = 2
            self.attr['hp'] = random.choice([10, 25, 50, 100, 250, 500, 1000])
        elif self.obj_type == 'scroll':
            self.usage = 2
            # TODO: Add attribute for eat it
        elif self.obj_type == 'potion':
            self.usage = 2
            # TODO: Add attribute for eat it