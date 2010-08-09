# dig.py by Dannil

import dm.cmd.wiz.wiz_cmd as wiz_cmd
import dm.obj.room        as room
import dm.util.area       as area

class Cmd(wiz_cmd.WizCmd):
    def __init__(self):
        wiz_cmd.WizCmd.__init__(self)

        self.add_rule("dig DIR")


    def rule_dig_DIR(self, body, args):
        dir = args[0]

        old_room = body.query_env()

        if not old_room:
            raise error.CmdFailed("You have no environment.\n")

        # Get data from the old room.
        old_code   = old_room.query("code_file")
        area_path  = old_room.query("area_path")
        old_coords = old_room.query("coords")

        # Get data for the new room.
        rel_coords    = area.conv_dir_to_rel_coords(dir)
        new_coords    = area.conv_rel_coords_to_abs(old_coords, rel_coords)
        new_room_path = "%s/%d,%d,%d" % (area_path, new_coords[0],
                                         new_coords[1], new_coords[2])
        reverse_dir   = area.REVERSE_DIRS[dir]

        body.recv_tag_text("Digging %s (%s) to %s...\n" %
                           (dir, rel_coords, new_coords))

        # Create the new room.
        print("Creating new room with path: '%s'" % area_path)
        new_room = room.Room([ old_code, area_path, new_coords ])

        # Set up the new room.
        new_room.set("coords", new_coords)

        # Load the new room in case it's not really new, 
        # otherwise save it.
        if new_room.load():
            body.recv_tag_text("Done. Existing room linked.\n")
        else:
            body.recv_tag_text("Done. Saving new room.\n")

        old_room.add_exit(dir,         old_code, area_path, new_coords)
        new_room.add_exit(reverse_dir, old_code, area_path, old_coords)

        new_room.save()
        old_room.save()
