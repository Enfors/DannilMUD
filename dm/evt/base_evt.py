# base_event.py by Dannil

class Evt:
    def __init__(self):
        self.broadcast = False
        self.doer      = None
        self.target    = None
        self.msg       = None

    def set_broadcast(self, bool):
        """Set the broadcast bool to True or False.

        Broadcast events are generally sent to a room. Non-broadcast events
        are sent to one or two objects - doer and / or target."""
        if not type(bool).__name__ == "bool":
            # todo: raise an exception here
            return False

        self.broadcast = bool
    

    def query_broadcast(self):
        """Return True if this is a broadcast event, otherwise False."""
        return self.broadcast


    def set_doer(self, doer):
        self.doer = doer


    def query_doer(self):
        return self.doer


    def set_target(self, target):
        self.target = target


    def query_target(self):
        return self.target


    def set_msg(self, msg):
        self.msg = msg


    def query_msg(self):
        return self.msg


    def activate(self):
        pass
