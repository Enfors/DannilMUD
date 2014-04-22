# room.py by Dannil

import dm.obj.container as container
import dm.obj.weapon    as weapon
import dm.sys.error     as error
import dm.daemon.obj_d  as obj_d

reverse_direction = {
    "north" : "south",
    "south" : "north",
    "east"  : "west",
    "west"  : "east",
    "up"    : "down",
    "down"  : "up"
    }

class Room(container.Container):
    def __init__(self, args):

        if len(args) < 3:
            raise error.InternalError("Room() needs at least 3 args: "
                                      "code_file, area_path and coords.")

        container.Container.__init__(self)

        self.set("object_type", "room")
        self.set("code_file",   args[0])
        self.set("area_path",   args[1])
        self.set("coords",      args[2])

        self.set("short", "A non-descript room")
        self.set("long",  "A very non-descript, generic-looking room.")

        self.set("exits", { })

        # Can accept any amount of bulk
        self.set("bulk_cap",   0)
        # Can accept any amount of weight
        self.set("weight_cap", 0)

        obj_d.OBJ_D.register(self)


    def add_exit(self, direction, code_file, area_path, coords):

        exits = self.query("exits")

        exits[direction] = [ code_file, area_path, coords ]

        self.set("exits", exits)
        
    
    def query_next_room_data(self, dir):
        return self.query("exits")[dir]


    def query_next_room(self, dir):
        data = self.query_next_room_data(dir)

        ref = "%s:%s:%d,%d,%d" % (data[0], data[1],
                                  data[2][0], data[2][1], data[2][2])

        next_room = obj_d.OBJ_D.request(ref)

        if not next_room:
            next_room = Room(data)
            next_room.load()

        return next_room
    

    def query_ref(self):
        coords = self.query("coords")
        return "%s:%s:%d,%d,%d" % (self.query("code_file"),
                                   self.query("area_path"),
                                   coords[0], coords[1], coords[2])
    

    def recv_text(self, text):
        """Receive text, and broadcast to everyone here."""
        for obj in self.contents:
            obj.recv_text(text)


    def save(self):
        container.Container.save(self, self.query_file_name())


    def load(self):
        return container.Container.load(self, self.query_file_name())


    def query_file_name(self):
        area_path = self.query("area_path")
        coords    = self.query("coords")

        if not area_path:
            raise error.InternalError("room.save(): Prop missing: area_path")

        if not coords:
            raise error.InternalError("room.save(): Prop missing: coords")

        return "%s/room_%d,%d,%d" % (area_path, coords[0], coords[1],
                                     coords[2])
        

        


    #def __repr__(self):
        #disp = self.query("short") + "\n"
        #disp += self.query("long") + "\n"
        #disp += "Obvious exits: "
        
        #exits = self.query("exits")

        #disp += ", ".join(exits.keys())

        #return disp



if __name__ == "__main__":
    lobby   = Room("Lobby")
    hall    = Room("Hall")
    kitchen = Room("Kitchen")

    lobby.add_exit("north", hall)
    hall.add_exit("east",   kitchen)

    weapon = weapon.Weapon()
    weapon.move_to_env(lobby)

    print(lobby)
    print(hall)
    print(kitchen)
