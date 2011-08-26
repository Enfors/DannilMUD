# body.py by Dannil

import dm.obj.container   as container
import dm.daemon.update_d as update_d

all_stats = ("dex", "end", "con", "str", "per", "foc", "int")

long_stat_names = {
    "dex" : "dexterity",
    "end" : "endurance",
    "con" : "contitution",
    "str" : "strength",
    "per" : "perception",
    "foc" : "focus",
    "int" : "intelligence"
    }

class Body(container.Container):
    def __init__(self):
        container.Container.__init__(self)
        self.set_name("unnamed")


    def set_name(self, name):
        self.name = name


    def query_name(self):
        return self.name
        

    def query_cap_name(self):
        return self.name.capitalize()


    def recv_tag_text(self, text, indent1 = 0, indent2 = 0,
                      leading_nl = False):
        text_d = update_d.update_d.request_obj("daemon.text_d",
                                               "TextD")

        text = text_d.convert_tag_text(text, self, None, 76, 
                                       indent1, indent2, leading_nl)
        return self.recv_text(text)


    def do_look(self):
        room = self.query_env()

        if not room:
            self.recv_text("You're.... nowhere. How'd that happen?\n")

        disp = "<room_short>%s</>\n<room_long>%s</>\n\n" % \
            (room.query("short"), room.query("long"))

        self.recv_tag_text(disp, indent1 = 2)

        disp = "<room_exits>Obvious exits: "

        exits = room.query("exits")

        if exits:
            disp += ", ".join(exits.keys())
        else:
            disp += "none"

        disp += "</>\n"

        contents = room.query_contents()

        for obj in contents:
            if obj == self:
                #disp += "(yourself)\n"
                continue
            else:
                disp += obj.query("short").capitalize() + ".\n"

        self.recv_tag_text(disp, indent1 = 2)


    def update(self):
        """This function is called on bodies after they are loaded,
        to update the object with new data, if data has been added
        since the object was last saved."""

        if not "ids" in self.props:
            self.props["ids"] = [ self.query_name() ]

        if not "stats" in self.props:
            stats = {
                "dex" : 10,
                "end" : 10,
                "con" : 10,
                "str" : 10,
                "per" : 10,
                "foc" : 10,
                "int" : 10
                }

            self.set("stats", stats)


    def set_stat(self, stat, value):
        self.props["stats"][stat] = value
        
        return value


    def query_stat(self, stat):
        return self.props["stats"][stat]


    def query_stats_disp(self):
        """Return a string containing our stats, suitable for printing."""
        
        disp = ""

        stats = self.props["stats"]

        for stat in all_stats:
            disp += "%-13s: %3d\n" % (long_stat_names[stat].capitalize(),
                                      stats[stat])

        return disp
