# diamond.py by Dannil - for object testing purposes only

import dm.obj.base as base

class Diamond(base.Base):
    def setup(self):
        self.set_name("diamond")
        self.set("ids", [ "diamond" ])
        self.set("short",      "a diamond")
        self.set("long",       "This is a shiny, sparkling diamond.")
        self.set("adjectives", [ "shiny", "sparkling" ])


def clone():
    return Diamond()
