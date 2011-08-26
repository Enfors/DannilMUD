# char.py by Dannil

import dm.obj.living as living

class Char(living.Living):
    def __init__(self):
        pass

    
    def setup(self):
        living.Living.setup(self)

        stats = {
            "dex" : 10,
            "end" : 10,
            "con" : 10,
            "str" : 10,
            "per" : 10,
            "foc" : 10,
            "int" : 10
            }

        self.set("stats", stats)


