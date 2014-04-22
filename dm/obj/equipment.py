# equipment.py by Dannil

import dm.obj.base as base

class Equipment(base.Base):
    def __init__(self):
        base.Base.__init__(self)

        self.set("short",  "Equipment")
        self.set("long",   "This is a generic piece of equipment.")
        self.set("weight", 200)
        self.set("bulk",   200)


#    def __repr__(self):
#        return base.Base.repr(self)


if __name__ == "__main__":
    eq = Equipment()
    print(eq)
