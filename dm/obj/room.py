# room.py by Dannil

import dm.obj.container as container

import dm.obj.weapon    as weapon

reverse_direction = {
    "north" : "south",
    "south" : "north",
    "east"  : "west",
    "west"  : "east",
    "up"    : "down",
    "down"  : "up"
    }

class Room(container.Container):
    def __init__(self, short = None):
        container.Container.__init__(self)

        self.set("object_type", "room")
        self.exits = { }

        #if short:
        #    self.set("short", short)
        #else:
        #    self.set("short", "A non-descript room")

        #self.set("long",  "A very non-descript, generic-looking room.")

        # Can accept any amount of bulk
        self.set("bulk_cap",   0)
        # Can accept any amount of weight
        self.set("weight_cap", 0)


    def add_exit(self, direction, target_room_path, both_ways = True):

        exits = self.exits

        target_room = update_d.update_d.request_obj(target_room_path,
                                                    "Room")
        
        if target_room.query("object_type") != "room":
            # todo: raise an exception here, remove print & return
            print("Target is not a room")
            return False

        exits[direction] = target_room_path

        #self.set("exits", exits)
        
        if both_ways:
            target_room.add_exit(reverse_direction[direction], self,
                                 both_ways = False)


    def recv_text(self, text):
        """Receive text, and broadcast to everyone here."""
        for obj in self.contents:
            obj.recv_text(text)

    
    def __repr__(self):
        disp = self.query("short") + "\n"
        disp += self.query("long") + "\n"
        disp += "Obvious exits: "
        
        exits = self.query("exits")

        disp += ", ".join(exits.keys())

        return disp



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
