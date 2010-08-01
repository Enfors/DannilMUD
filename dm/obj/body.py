# body.py by Dannil

import dm.obj.container as container

class Body(container.Container):
    def __init__(self):
        set_name("unnamed")


    def set_name(self, name):
        self.name = name


    def query_name(self):
        return self.name
        
