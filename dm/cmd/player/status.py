# status.py by Dannil

import dm.cmd.player.player_cmd as player_cmd

class Cmd(player_cmd.PlayerCmd):
    def __init__(self):
        player_cmd.PlayerCmd.__init__(self)

        self.add_rule("status")


    def rule_status(self, user):
        disp = "Wizard : "
        if user.query("is_wiz"):
            disp += "Yes\n"
        else:
            disp += "No\n"

        disp += "Admin  : "
        if user.query("is_admin"):
            disp += "Yes\n"
        else:
            disp += "No\n"

        user.recv_text(disp)
