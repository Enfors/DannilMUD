# quit.py by Dannil

import dm.cmd.player.player_cmd as player_cmd

class Cmd(player_cmd.PlayerCmd):
    def __init__(self):
        player_cmd.PlayerCmd.__init__(self)
        
        self.add_rule("quit")


    def rule_quit(self, body, args):
        #body.close_con()
        body.end()
        
        env = body.query_env()

        if env:
            env.recv_text("%s left the game.\n" % body.query_cap_name())
        
