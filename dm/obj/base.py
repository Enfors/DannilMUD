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

        if func_name in dir(self):
            return eval("self.%s()" % func_name)
        else:
            return self.props[prop]


if __name__ == "__main__":
    obj = Base()
