# look.py by Dannil

import dm.cmd.player.player_cmd as player_cmd

class Cmd(player_cmd.PlayerCmd):
    def __init__(self):
        player_cmd.PlayerCmd.__init__(self)

        self.add_rule("look")


    def rule_look(self, user):
        room = user.query_env()

        if not room:
            user.recv_text("You're.... nowhere. How'd that happen?\n")

        disp = "%s\n%s\n" % (room.query("short"), room.query("long"))

        disp += "Obvious exits: "

        exits = room.query("exits")

        if exits:
            disp += ", ".join(exits.keys())
        else:
            disp += "none"

        disp += "\n"

        contents = room.query_contents()

        for obj in contents:
            if obj == user:
                disp += "(yourself)\n"
            else:
                disp += obj.query("short") + "\n"

        user.recv_text(disp)
