class Object():
    def __init__(self, x, y, level):
        self.x = x
        self.y = y
        self.level = level
        self.attr = {}
        
        self._gen_obj()
    
    def _gen_obj(self):
        self.obj_type = None