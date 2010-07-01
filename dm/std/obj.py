# obj.py by Dannil
#
# This is one of the most important files in the MUD - the standard game
# object. All in-game objects should (probably indirectly) inherit this
# class.
#

class Obj:
    """The basic game object, which all other objects inherit."""
    def __init__(self):
        self.set_short("ordinary-looking object")
        self.set_long( \
            "This is a very ordinary-looking object. " \
            "It has no distinguishable features at all. " \
            "It is, in fact, so utterly plain and uninteresting " \
            "that you can't even tell what it is. And nobody cares.")
            

    def set_short(self, short):
        """Sets the short description of the object."""
        self.short = short


    def query_short(self):
        """Returns the short description of the object."""
        return self.short


    def set_long(self, long):
        """Sets the long description of the object."""
        self.long = long
