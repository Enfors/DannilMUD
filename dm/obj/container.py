# container.py by Dannil

import dm.obj.base as base

import dm.obj.equipment as equipment
import dm.obj.weapon    as weapon

class Container(base.Base):
    """This class implements containers of all sorts.

Bags, sacks, barrels and such inherit this class. But also room
(which contain what is in the room) as well as living (which
contains the living's inventory)."""
    def __init__(self):
        base.Base.__init__(self)
        
        self.contents = [ ]

        self.set("bulk_cap",   0)
        self.set("weight_cap", 1000)

        
    def add_content(self, obj):
        if not self.can_add_content(obj):
            return False
        else:
            self.contents.append(obj)
            obj.set_env(self)
            return True

    
    def remove_content(self, obj):
        if obj in self.contents:
            self.contents.remove(obj)

        return True


    def can_add_content(self, obj):
        """Return True if the specified object can be held in this container.
Otherwise, False is returned. Both weight and bulk is checked."""

        obj_weight = obj.query("weight") or 1
        obj_bulk   = obj.query("bulk")   or 1

        held_weight = self.query_held_weight()
        held_bulk   = self.query_held_bulk()

        weight_cap  = self.query("weight_cap")
        bulk_cap    = self.query("bulk_cap")

        if weight_cap and (obj_weight + held_weight > weight_cap):
            # todo: raise TooHeavy exception here
            return False
        
        if bulk_cap and (obj_bulk + held_bulk > bulk_cap):
            # todo: raise DoesntFit exception here
            return False

        return True


    def query_contents(self):
        return self.contents


    def query_held_weight(self):
        held_weight = 0

        for obj in self.contents:
            try:
                held_weight += obj.query("weight")
            except TypeError:
                continue

        return held_weight


    def query_held_bulk(self):
        held_bulk = 0

        for obj in self.contents:
            try:
                held_bulk += obj.query("bulk")
            except TypeError:
                continue

        return held_bulk


    #def __repr__(self):
        #disp = base.Base.__repr__(self)
        #contents_disp = ""

        #for obj in self.contents:
        #    contents_disp += "  +-%s\n" % obj.query("short")

        #if len(contents_disp) == 0:
        #    return disp + "  | No contents.\n"
        #else:
        #    return "%s  | Contents: (weight: %d)\n%s" % \
        #        (disp, self.query_held_weight(), contents_disp)



if __name__ == "__main__":
    bag = Container()
    weapon = weapon.Weapon()
    eq     = equipment.Equipment()

    bag.add_contents(weapon)
    bag.add_contents(eq)
    print(bag)
