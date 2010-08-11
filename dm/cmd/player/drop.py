# drop.py by Dannil

import dm.cmd.player.player_cmd as player_cmd

class Cmd(player_cmd.PlayerCmd):
    def __init__(self):
        player_cmd.PlayerCmd.__init__(self)

        self.add_rule("drop IOBJ")

    def rule_drop_IOBJ(self, body, args):
        obj = args[0]

        self.do_drop(body, obj)


    def do_drop(self, body, obj):
        room = body.query_env()

        if not room:
            body.recv_tag_text("You can't drop anything here.\n")
            return False
        
        if obj.move_to_env(room):
            # todo: insert events here
            body.recv_tag_text("Dropped.\n")
        else:
            body.recv_tag_text("You can't drop that.\n")

