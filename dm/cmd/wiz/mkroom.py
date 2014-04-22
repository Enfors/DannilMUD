# mkroom.py by Dannil

import os

import dm.cmd.wiz.wiz_cmd as wiz_cmd
import dm.obj.room        as room
import dm.sys.error       as error


class Cmd(wiz_cmd.WizCmd):
    def __init__(self):
        wiz_cmd.WizCmd.__init__(self)

        self.add_rule("mkroom PATH")


    def rule_mkroom_PATH(self, body, args):
        body.recv_tag_text("Creating room in %s...\n" % args)

        area_path = args[0]

        if not os.path.isdir(area_path):
            raise error.BuildingError("mkroom: Directory %s is not valid." %
                                      area_path)

        new_room = room.Room([ "obj.room", area_path, [ 0, 0, 0] ])

        new_room.set("short", "An empty room")
        new_room.set("long",  "This room is filled with a whole lot of "
                     "nothing. As far as the eye can see.")

        new_room.save()

        body.move_to_env(new_room)
