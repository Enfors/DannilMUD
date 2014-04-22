# look.py by Dannil

import dm.cmd.player.player_cmd as player_cmd

class Cmd(player_cmd.PlayerCmd):
    def __init__(self):
        player_cmd.PlayerCmd.__init__(self)

        self.add_rule("look")
        self.add_rule("look at OBJ")


    def rule_look(self, body, args):
        body.do_look()


    def rule_look_at_OBJ(self, body, args):
        obj = args[0]
        body.recv_tag_text(obj.query_desc() + "\n")
