# go.py by Dannil

import dm.cmd.player.player_cmd as player_cmd
import dm.evt.leave_evt         as leave_evt
import dm.evt.enter_evt         as enter_evt

class Cmd(player_cmd.PlayerCmd):
    def __init__(self):
        player_cmd.PlayerCmd.__init__(self)
        
        self.add_rule("go DIR")


    def rule_go_DIR(self, body, args):
        env = body.query_env()

        dir = args[0]

        if not env:
            body.recv_tag_text("You cannot simply walk away from "
                               "this place.")
            return False

        leave_event = leave_evt.LeaveEvt()
        leave_event.set_operators([body])
        leave_event.set_text("$N0 $v0try to go %s, but that hasn't "
                             "been implemented yet.\n" % dir)
        leave_event.activate()

