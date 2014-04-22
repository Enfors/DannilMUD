# lobby.py by Dannil

import dm.obj.room as room

class Lobby(room.Room):
    def __init__(self):
        room.Room.__init__(self)

        self.set("short", "The lobby")
        self.set("long",  "This place is empty. A friggin void.")
