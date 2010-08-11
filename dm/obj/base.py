# base.py by Dannil
#
# This is one of the most important files in the MUD - the standard game
# object. All in-game objects should (probably indirectly) inherit this
# class.
#

import os, pickle

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

        self.set("ids", [ ])

        # Env = environment = which room the object is in.
        self.env = None

        self.setup()


    def setup(self):
        """This function is called at the end of __init__. Its purpose
        is to be overloaded by "leaf" classes, to be used to set
        things up at object creation time."""
        pass


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


    def set_name(self, name):
        """Sets the name of the object. If the object doesn't already
        have an id identical to the name, such an id is added."""
        self.props[name] = name.lower()

        ids = self.query("ids")

        if not ids:
            ids = [ ]
        
        if not name in ids:
            ids.append(ids)

        self.set_ids(ids)


    def query_name(self):
        return self.name


    def set_ids(self, ids):
        # If the argument isn't a list, then make a list of it.
        if type(ids).__name__ == "str":
            ids = [ ids ]

        self.props["ids"] = ids


    def move_to_env(self, target_env):
        """Move the specified object to the specified environment.

can_add_content() is called on the target environment first, to
make sure that it can accept the object being moved.

RETURNS:
  True  : If the move was successful
  False : If the move failed
"""
        old_env = self.query_env()
        if target_env.can_add_content(self):
            if target_env.add_content(self):
                if old_env:
                    old_env.remove_content(self)

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


    def recv_tag_text(self, text, indent1 = 0, indent2 = 0,
                      leading_nl = False):
        pass


    def save(self, file_name):
        #print("[base] Saving object under filename '%s'..." % file_name)
        file = open(file_name, "wb")
        try:
            pickle.dump(self.props, file)
        finally:
            file.close()

        return True


    def load(self, file_name):
        """Loads properties from the specified file and stores them
        as this object's properties.

        RETURNS:
        - True, if the file exists and can be successfully loaded
        - False, otherwise."""
        if not os.path.exists(file_name):
            return False

        file = open(file_name, "rb")
        try:
            self.props = pickle.load(file)
        finally:
            file.close()

        return True


    def query_ref(self):
        raise error.InternalError("Class has no overloaded query_ref() "
                                  "function.")


    def query_desc(self):
        """When someone looks at an object, this is the function
        that gets called to return the object's description."""
        return self.query("long")


    def end(self):
        """Call this function when you want to remove an object.
        It will not actually be removed - you have to delete all
        references to it for that."""

        if self.env:
            self.env.remove_content(self)


    #def __repr__(self):
        #val = self.query("short") + "\n"

        #room = self.env

        #if room:
        #    room = room.query("short")
        #else:
        #    room = "None"

        #val += "  | Environment: %s\n" % room

        #prop_disp = ""

        #for key in self.props.keys():
        #    prop_disp += "  +-%-20s: %s\n" % (key, str(self.props[key]))

        #if len(prop_disp):
        #    val += "  | Properties:\n" + prop_disp
        #else:
        #    val += "  | No properties.\n"
        
        #return val
            

if __name__ == "__main__":
    obj = Base()
    print(obj)
