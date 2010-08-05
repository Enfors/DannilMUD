# wizme.py by Dannil

import dm.cmd.player.player_cmd as player_cmd

class Cmd(player_cmd.PlayerCmd):
    def __init__(self):
        player_cmd.PlayerCmd.__init__(self)

        self.add_rule("wizme")


    def rule_wizme(self, body, args):
        if body.query_name() == "dannil":
            body.set("is_wiz",   1)
            body.set("is_admin", 1)
            body.recv_text("Done. You are now a Wizard.\n")
        else:
            body.recv_text("Sorry, I can not allow that.\n")
