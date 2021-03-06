# base_event.py by Dannil

import dm.daemon.update_d as update_d

special_verbs = {
    "go"     : "goes",
    "try"    : "tries",
}

class Evt:
    def __init__(self):
        self.broadcast  = True
        self.operators  = ( )
        self.excepted_observers = [ ]
        self.doer       = None
        self.target     = None
        self.text       = ( )
        self.indent1    = 0      # Indentation for first line
        self.indent2    = 0      # Indentation for consequtive lines
        self.leading_nl = False
        self.text_d     = update_d.update_d.request_obj("daemon.text_d",
                                                        "TextD")

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


    def set_excepted_observers(self, excepted_observers):
        """Set a list of bodies which should never see the event."""
        self.excepted_observers = excepted_observers


    def set_doer(self, doer):
        self.doer = doer


    def query_doer(self):
        return self.doer


    def set_target(self, target):
        self.target = target


    def query_target(self):
        return self.target


    def set_text(self, text):
        #self.text = self.text_d.split_with_tags(text)
        self.text = text.split(" ")


    def query_text(self):
        return " ".join(self.text)


    def set_leading_nl(self, bool):
        self.leading_nl = bool


    def query_leading_nl(self):
        return self.leading_nl


    def query_observer_text(self, observer):
        text = [ ]

        if observer in self.operators:
            observer_num = self.operators.index(observer)
        else:
            observer_num = -1

        for word in self.text:
            dollar_pos = word.find("$")

            if dollar_pos != -1:
                part = word[:dollar_pos] + \
                    self._handle_var(word[dollar_pos + 1:], observer_num)

                text.append(part)
            else:
                text.append(word)

        return " ".join(text)


    def _handle_var(self, word, observer_num):
        try:
            operator_num = int(word[1])
        except ValueError:
            raise error.InternalError("Expected number in position 1 "
                                      "of '%s'." % word)

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
            verb, rest = self._separate_nonalphas(verb)

            #if verb[-1] == "y":
            #    verb = verb[:-1] + "ie"

            if verb in special_verbs:
                return special_verbs[verb] + rest
            else:
                return verb + "s" + rest


    def _separate_nonalphas(self, text):
        """If text is 'foo!', return 'foo', '!'."""
        for i in range(0, len(text)):
            if not text[i].isalpha():
                rest = text[i:]
                text = text[:i]

                return text, rest

        return text, ""
    

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
            if recipient not in self.excepted_observers:
                self._notify_recipient(recipient)


    def _notify_recipient(self, recipient):
        text = self.query_observer_text(recipient)

        recipient.recv_tag_text(text,
                                indent1    = self.indent1,
                                indent2    = self.indent2,
                                leading_nl = self.leading_nl)


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

