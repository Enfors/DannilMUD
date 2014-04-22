# who.py by Dannil

import dm.cmd.player.player_cmd as player_cmd
import dm.daemon.update_d as update_d

class Cmd(player_cmd.PlayerCmd):
    def __init__(self):
        player_cmd.PlayerCmd.__init__(self)

        self.add_rule("who")


    def rule_who(self, body, args):
        user_man = update_d.update_d.request_obj("sys.user_man",
                                                 "UserMan")

        users = user_man.query_users()

        disp = "Who's loggged on\n" \
            "================\n"
        
        for u in users.values():
            disp += u.query_cap_name() + "\n"

        body.recv_tag_text(disp)

