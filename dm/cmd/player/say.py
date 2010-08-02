# say.py by Dannil

import dm.cmd.player.player_cmd as player_cmd

class Cmd(player_cmd.PlayerCmd):
    def __init__(self):
        player_cmd.PlayerCmd.__init__(self)

        self.add_rule("say")
        self.add_rule("say STR")


    def rule_say(self, user):
        user.recv_text("What do you want to say?\n")


    def rule_say_STR(self, user, str):
        env = user.query_env()

        if not env:
            user.recv_text("There is noone here to talk to.\n")
            return False

        env.recv_text("%s says: %s\n" % (user.query_cap_name(), str))
