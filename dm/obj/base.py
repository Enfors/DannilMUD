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
        self.props[prop] = value


    def query(self, prop):
        """Return the value of the specified prop."""
        value = self.props[prop]
        return value


if __name__ == "__main__":
    obj = Base()
    obj.set("Foo", "bar")
    print(obj.query("Foo"))
    print(obj.query("short"))
    print(obj.query("long"))

