# go.py by Dannil

import dm.cmd.player.player_cmd as player_cmd
import dm.evt.move_evt          as move_evt
import dm.daemon.update_d       as update_d
import dm.sys.error             as error

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

        if not self.check_if_legal_exit(body, env, dir):
            return False

        leave_event = move_evt.LeaveEvt()
        leave_event.set_operators([body])
        leave_event.set_text("$N0 $v0go %s.\n" % dir)
        leave_event.activate()

        dest_room = self.query_dest_room(env, dir)

        body.move_to_env(dest_room)

        enter_event = move_evt.EnterEvt()
        enter_event.set_operators([body])
        enter_event.set_excepted_observers([body])
        enter_event.set_text("$N0 $v0arrive.\n")
        enter_event.activate()

        body.do_look()

        return True


    def check_if_legal_exit(self, body, env, dir):
        exits = env.query("exits")

        if dir in exits.keys():
            return True
        else:
            body.recv_tag_text("You cannot go %s here.\n" % dir)
            return False


    def query_dest_room(self, env, dir):
        return env.query_next_room(dir)
