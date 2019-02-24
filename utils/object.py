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

ATTR_LIST = ['atk', 'atk_mul', 'dfn', 'dfn_mul', 'max_hp']
ATTR_USE_LIST = ['atk', 'dfn', 'hp', 'max_hp']

class Object():
    def __init__(self, x, y, level, key_item=False):
        self.x = x
        self.y = y
        self.level = level
        self.key_item = key_item
        self.attrs = {}
        
        if self.key_item:
            self.obj_type = 'key_item'
        else:
            self._gen_obj()
    
    def __repr__(self):
        attr_str = []
        for k in self.attrs:
            attr_str.append("{0}: {1}".format(k, self.attrs[k]))
        return self.obj_type + "(" + " ".join(attr_str)
        
    def __str__(self):
        return self.obj_type
    
    def _gen_obj(self):
        self.obj_type = random.choice(OBJ_LIST)
        self.usage = 0
        if self.obj_type == 'money':
            self.attrs['score'] = random.randint(10, (self.level ** 2) * 100)
        elif self.obj_type in ['weapon', 'wand']:
            self.usage = 1
            self.attrs['atk'] = random.randint(10, 10 + self.level * 15)
        elif self.obj_type == 'armor':
            self.usage = 1
            self.attrs['dfn'] = random.randint(10, 10 + self.level * 15)
        elif self.obj_type in ['ring', 'amulet']:
            self.usage = 1
            k = 1 + min(self.level // 13, 2)
            choice_attr = random.sample(ATTR_LIST, k=k)
            for attr in choice_attr:
                if 'mul' in attr:
                    self.attrs[attr] = 2 + random.randint(0, self.level // 13)
                else:
                    self.attrs[attr] = random.randint(10, 10 + self.level * 15)
        elif self.obj_type == 'edible':
            self.usage = 2
            self.attrs['hp'] = random.choice([10, 25, 50, 100, 250, 500, 1000])
        elif self.obj_type == 'scroll':
            self.usage = 2
            attr = random.choice(ATTR_USE_LIST)
            self.attrs[attr] = random.randint(10, 10 + self.level * 15)
        elif self.obj_type == 'potion':
            self.usage = 2
            attr = random.choice(ATTR_USE_LIST)
            self.attrs[attr] = random.randint(10, 10 + self.level * 15)