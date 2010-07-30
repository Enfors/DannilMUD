# weapon.py by Dannil

import dm.obj.equipment    as equipment
import dm.obj.light_source as light_source

class Weapon(equipment.Equipment):
    def __init__(self):
        equipment.Equipment.__init__(self)

        self.set("short", "Weapon")
        self.set("long",  "A non-descript weapon.")


if __name__ == "__main__":
    weapon = Weapon()
    print(weapon)
