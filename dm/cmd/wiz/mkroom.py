# mkroom.py by Dannil

import dm.cmd.wiz.wiz_cmd as wiz_cmd
import dm.obj.room        as room

class Cmd(wiz_cmd.WizCmd):
    def __init__(self):
        wiz_cmd.WizCmd.__init__(self)

        self.add_rule("mkroom PATH")


    def rule_mkroom_PATH(self, body, args):
        body.recv_tag_text("Creating room... well, not really: %s\n" % args)

        new_room = room.Room()

        new_room.set("short", "An empty room")
        new_room.set("long",  "This room is filled with a whole lot of "
                     "nothing. As far as the eye can see.")

        body.move_to_env(new_room)
