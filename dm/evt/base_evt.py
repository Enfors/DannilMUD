# base_event.py by Dannil

class Evt:
    def __init__(self):
        self.broadcast = True
        self.operators = ( )
        self.doer      = None
        self.target    = None
        self.text      = ( )

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


    def set_operators(self, operators):
        self.operators = operators


    def query_operators(self, operators):
        return self.operators


    def set_doer(self, doer):
        self.doer = doer


    def query_doer(self):
        return self.doer


    def set_target(self, target):
        self.target = target


    def query_target(self):
        return self.target


    def set_text(self, text):
        self.text = text.split(" ")


    def query_text(self):
        return " ".join(self.text)


    def query_observer_text(self, observer):
        text = [ ]

        if observer in self.operators:
            observer_num = self.operators.index(observer)
        else:
            observer_num = -1

        for word in self.text:
            if word[0] == "$":
                text.append(self._handle_var(word[1:], observer_num))
            else:
                text.append(word)

        return " ".join(text)


    def _handle_var(self, word, observer_num):
        # todo: handle ValueError on the following line
        operator_num = int(word[1])
        if word[0] == "N":      # Name (capitalize "You")
            return self._handle_name(word[2:], observer_num,
                                     operator_num, capitalize = True)

        if word[0] == "n":      # name (don't capitalize "you")
            return self._handle_name(word[2:], observer_num,
                                     operator_num, capitalize = False)

        elif word[0] == "v":    # Verb
            return self._handle_verb(word[2:], observer_num,
                                     operator_num)


    def _handle_name(self, word, observer_num, operator_num, capitalize):

        if operator_num == observer_num:
            if capitalize:
                return "You"
            else:
                return "you"
        else:
            return self._query_name(self.operators[operator_num])


    def _handle_verb(self, verb, observer_num, operator_num):
        if observer_num == operator_num:
            return verb
        else:
            return verb + "s"
    

    def _query_name(self, operator):
        """Because of this function, operator can be both string (for
        testing purposes) as well as an object."""
        if type(operator).__name__ == "str":
            return operator
        else:
            return operator.query_cap_name()

        
    def activate(self):
        recipients = [ ]

        if self.broadcast:
            rooms = self._query_operator_rooms()

            for room in rooms:
                recipients += self._query_room_occupants(room)
        else:
            recipients = self.operators

        for recipient in recipients:
            self._notify_recipient(recipient)


    def _notify_recipient(self, recipient):
        text = self.query_observer_text(recipient)

        # todo: replace recv_text() with higher level function
        recipient.recv_text(text + "\n")


    def _query_operator_rooms(self):
        rooms = [ ]

        for operator in self.operators:
            room = operator.query_env()

            if not room:
                continue

            if not room in rooms:
                rooms.append(room)

        return rooms


    def _query_room_occupants(self, room):
        occupants = [ ]

        for occupant in room.query_contents():
            if not occupant in occupants:
                occupants.append(occupant)

        return occupants


    
if __name__ == "__main__":
    event = Evt()
    event.set_broadcast(True)
    event.set_operators(("Indra", "Alvin"))
    event.set_text("$N0 $v0kick $n1 on the leg.")
    print(event.query_text())
    print(event.query_observer_text("Indra"))
    print(event.query_observer_text("Alvin"))

    event.set_text("$N1 $v1get upset, and $v1wrestle $n0 to the ground.")
    print("")
    print(event.query_observer_text("Indra"))
    print(event.query_observer_text("Alvin"))

