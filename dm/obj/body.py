# body.py by Dannil

import dm.obj.container as container

class Body(container.Container):
    def __init__(self):
        container.Container.__init__(self)
        self.set_name("unnamed")


    def set_name(self, name):
        self.name = name


    def query_name(self):
        return self.name
        

    def query_cap_name(self):
        return self.name.capitalize()
