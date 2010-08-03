# body.py by Dannil

import dm.obj.container   as container
import dm.daemon.update_d as update_d

class Body(container.Container):
    def __init__(self):
        container.Container.__init__(self)
        self.set_name("unnamed")


    def set_name(self, name):
        self.name = name


    def query_name(self):
        return self.name
        

    def query_cap_name(self):
        return self.name.capitalize()


    def recv_tag_text(self, text, indent1 = 0, indent2 = 0,
                      leading_nl = False):
        text_d = update_d.update_d.request_obj("daemon.text_d",
                                               "TextD")

        text = text_d.convert_tag_text(text, self, None, 76, 
                                       indent1, indent2, leading_nl)
        return self.recv_text(text + "\n")

