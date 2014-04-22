# emote.py by Dannil

import dm.cmd.player.player_cmd as player_cmd
import dm.evt.emote_evt         as emote_evt

class Cmd(player_cmd.PlayerCmd):
    def __init__(self):
        player_cmd.PlayerCmd.__init__(self)

        self.add_rule("emote")
        self.add_rule("emote STR")


    def rule_emote(self, body, args):
        user.recv_text("What do you want to emote?\n")

        
    def rule_emote_STR(self, body, args):
        emote_event = emote_evt.EmoteEvt()
        emote_event.set_operators([body])
        emote_event.set_text("<emote>%s %s</>\n" % 
                             (body.query_cap_name(), " ".join(args)))
        emote_event.activate()

