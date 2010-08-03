# color_d.py by Dannil

import dm.daemon.base_daemon as base_daemon

csi   = "["
reset = "0m"

color_codes = {
    "reset"        : csi + "0m",
    "red"          : csi + "31m",
    "red-bold"     : csi + "1;31m",
    "green"        : csi + "32m",
    "green-bold"   : csi + "1;32m",
    "yellow"       : csi + "33m",
    "yellow-bold"  : csi + "1;33m",
    "blue"         : csi + "34m",
    "blue-bold"    : csi + "1;34m",
    "magenta"      : csi + "35m",
    "magenta-bold" : csi + "1;35m",
    "cyan"         : csi + "36m",
    "cyan-bold"    : csi + "1;36m",
    }

class ColorD(base_daemon.Daemon):
    def __init__(self):
        base_daemon.Daemon.__init__(self)
        
        self.color_config = {
            "/"          : "reset",
            "emote"      : "green",
            "room_short" : "yellow-bold",
            "room_long"  : "yellow",
            "room_exits" : "yellow",
            "say"        : "green"
            }
    
    
    def query_tag_code(self, tag, prefs = None):
        global color_codes

        if not tag in self.color_config:
            return ""

        color = self.color_config[tag]

        if not color in color_codes:
            return ""

        return color_codes[color]



if __name__ == "__main__":
    color_d = ColorD()

    print("Time for some %sgreen!%s" % (color_d.query_tag_code("say", None),
                                        reset))
