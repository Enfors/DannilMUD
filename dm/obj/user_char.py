# user_char.py by Dannil

import os, pickle, time

import dm.obj.body        as body
import dm.daemon.update_d as update_d

class UserChar(body.Body):
    def __init__(self, con):
        body.Body.__init__(self)
        self.set_name(con.login)
        self.set_con(con)
        self.set("long", "%s is a generic-looking user." %
                 self.query_cap_name())
        self.set("last_login", time.time())

    
    def update(self):
        body.Body.update(self)

        self.set("long", "%s is a generic-looking user." %
                 self.query_cap_name())


    def set_name(self, name):
        self.name = name


    def query_name(self):
        return self.name


    def recv_text(self, text):
        self.con.write(text)

    
    def set_con(self, con):
        self.con = con
        con.set_user_char(self)


    def query_con(self, con):
        return self.con


    def end(self):
        body.Body.end(self)
        self.close_con()


    def close_con(self):
        print("[user_char] close_con()")
        self.con.end_after_write()


    def con_closed(self):
        """Called by net.ConMan to tell us that the connection has been
        closed."""
        user_man = update_d.update_d.request_obj("sys.user_man",
                                                 "UserMan")
        user_man.end_user(self)


    def save(self):
        if not len(self.name):
            raise SaveErrorNoName

        file_name = self.query_file_name()

        body.Body.save(self, file_name)

        print("[user] %s saved." % self.query_cap_name())


    def load(self):
        if not len(self.name):
            pass                # todo: do something interesting here

        file_name = "user/%s" % self.query_name()
        
        body.Body.load(self, file_name)

        return self

    
    def query_file_name(self):
        return "user/%s" % self.query_name()
