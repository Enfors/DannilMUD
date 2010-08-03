# street1.py by Dannil

import dm.world.ooc.room.base_ooc_room as base_ooc_room

class Room(base_ooc_room.OOCRoom):
    def setup(self):
        self.set("short", "A dark street")
        self.set("long", "A dark street, covered with withered "
                 "leaves runs east and west. "
                 "The lack of light makes it very hard to make out "
                 "much of the murky surroundings save for a mansion, "
                 "strangely out of place on the north side of the "
                 "street. "
                 "A large wooden door, left slightly ajar, allows "
                 "entry for those who are not afraid to enter "
                 "strange mansions on dark streets.")

