# area.py by Dannil

X = 0 # East  = 1, west  = -1
Y = 1 # North = 1, south = -1
Z = 2 # Up    = 1, down  = -1

REVERSE_DIRS = {
    "north" : "south",
    "south" : "north",
    "east"  : "west",
    "west"  : "east",
    "up"    : "down",
    "down"  : "up"
    }


def conv_rel_coords_to_abs(start_coords, rel_coords):
    """Given a room's absolute coords (start_coords) and relative
    coords, return the other room's absolute coords."""
    abs_coords = [ None, None, None ]

    for i in range(0, len(start_coords)):
        abs_coords[i] = start_coords[i] + rel_coords[i]

    return abs_coords


def conv_dir_to_rel_coords(dir):
    """Convert a direction to relative coords."""
    rel_coords = [0, 0, 0]

    if dir == "north":
        rel_coords[Y] = -1
    elif dir == "south":
        rel_coords[Y] = 1
    elif dir == "west":
        rel_coords[X] = -1
    elif dir == "east":
        rel_coords[X] = 1
    elif dir == "up":
        rel_coords[Z] = 1
    elif dir == "down":
        rel_coords[Z] = -1
    else:
        raise error.InternalError("Invalid direction '%s'" % dir)

    return rel_coords

