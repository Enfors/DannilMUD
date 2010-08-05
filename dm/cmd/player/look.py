# look.py by Dannil

import dm.cmd.player.player_cmd as player_cmd

class Cmd(player_cmd.PlayerCmd):
    def __init__(self):
        player_cmd.PlayerCmd.__init__(self)

        self.add_rule("look")


    def rule_look(self, body, args):
        room = body.query_env()

        if not room:
            body.recv_text("You're.... nowhere. How'd that happen?\n")

        disp = "<room_short>%s</>\n<room_long>%s</>\n\n" % \
            (room.query("short"), room.query("long"))

        body.recv_tag_text(disp, indent1 = 2)

        disp = "<room_exits>Obvious exits: "

        exits = room.query("exits")

        if exits:
            disp += ", ".join(exits.keys())
        else:
            disp += "none"

        disp += "</>\n"

        contents = room.query_contents()

        for obj in contents:
            if obj == body:
                #disp += "(yourself)\n"
                continue
            else:
                disp += obj.query("short") + "\n"

        body.recv_tag_text(disp, indent1 = 2)
