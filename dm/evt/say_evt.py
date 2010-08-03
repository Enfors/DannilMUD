# say_evt.py by Dannil

import dm.evt.com_evt as com_evt

class SayEvt(com_evt.ComEvt):
    def __init__(self):
        com_evt.ComEvt.__init__(self)
        self.indent2 = 4
