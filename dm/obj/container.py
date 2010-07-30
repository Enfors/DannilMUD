# container.py by Dannil

import dm.obj.base as base

class Container(base.Base):
    """This class implements containers of all sorts.

Bags, sacks, barrels and such inherit this class. But also room
(which contain what is in the room) as well as living (which
contains the living's inventory)."""
    def __init__(self):
        base.Base.__init__(self)
        
        self.contents = [ ]

        self.set("bulk_cap",   1)
        self.set("weight_cap", 1)
