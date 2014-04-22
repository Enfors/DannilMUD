# get.py by Dannil

import dm.cmd.player.player_cmd as player_cmd

class Cmd(player_cmd.PlayerCmd):
    def __init__(self):
        player_cmd.PlayerCmd.__init__(self)

        self.add_rule("get ROBJ")

    def rule_get_ROBJ(self, body, args):
        obj = args[0]

        self.do_get(body, obj)


    def do_get(self, body, obj):
        if obj.move_to_env(body):
            # todo: insert events here
            body.recv_tag_text("Taken.\n")
        else:
            body.recv_tag_text("You can't take that.\n")

