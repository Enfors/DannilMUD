# base.py by Dannil
#
# This is one of the most important files in the MUD - the standard game
# object. All in-game objects should (probably indirectly) inherit this
# class.
#

class Base:
    """The basic game object, which all other objects inherit."""

    def __init__(self):
        self.props = { }
        self.set("short", "ordinary-looking object")
        self.set("long",
            "This is a very ordinary-looking object. " \
            "It has no distinguishable features at all. " \
            "It is, in fact, so utterly plain and uninteresting " \
            "that you can't even tell what it is. And nobody cares.")

        # Env = environment = which room the object is in.
        self.env = None


    def set(self, prop, value):
        """Set the property prop to the specified value."""
        func_name = "set_%s" % prop

        if func_name in dir(self):
            eval("self.%s(value)" % func_name)
        else:
            self.props[prop] = value


    def query(self, prop):
        """Return the value of the specified prop."""
        func_name = "query_%s" % prop

        try:
            if func_name in dir(self):
                return eval("self.%s()" % func_name)
            else:
                if prop in self.props:
                    return self.props[prop]
                else:
                    return None
        except KeyError:
            return None


    def move_to_env(self, target_env):
        """Move the specified object to the specified environment.

can_add_contents() is called on the target environment first, to
make sure that it can accept the object being moved.

RETURNS:
  True  : If the move was successful
  False : If the move failed
"""
        if target_env.can_add_contents(self):
            if target_env.add_contents(self):
                self.env = target_env
                return True

        return False


    def set_env(self, env):
        """Puts the object in the specified environment (room, bag, ...)"""
        self.env = env


    def query_env(self):
        """Return the object's environment (room, bag, ...)."""
        return self.env


    def recv_text(self, text):
        """Send a message to this object.
        
        This function should probably be overridden."""
        pass


    def __repr__(self):
        val = self.query("short") + "\n"

        room = self.env

        if room:
            room = room.query("short")
        else:
            room = "None"

        val += "  | Environment: %s\n" % room

        prop_disp = ""

        for key in self.props.keys():
            prop_disp += "  +-%-20s: %s\n" % (key, str(self.props[key]))

        if len(prop_disp):
            val += "  | Properties:\n" + prop_disp
        else:
            val += "  | No properties.\n"
        
        return val
            

if __name__ == "__main__":
    obj = Base()
    print(obj)
