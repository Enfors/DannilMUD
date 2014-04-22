# weapon.py by Dannil

import dm.obj.equipment      as equipment
import dm.obj.m_light_source as m_light_source

class Weapon(equipment.Equipment, m_light_source.LightSource):
    def __init__(self):
        equipment.Equipment.__init__(self)
        m_light_source.LightSource.__init__(self)

        self.set("short", "Weapon")
        self.set("long",  "A non-descript weapon.")
        self.set("weight", 400)
        self.set("bulk",   400)


if __name__ == "__main__":
    weapon = Weapon()
    print(weapon)
