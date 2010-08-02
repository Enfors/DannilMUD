# user_char.py by Dannil

import os, pickle

import dm.obj.body        as body
import dm.daemon.update_d as update_d

class UserChar(body.Body):
    def __init__(self, con):
        body.Body.__init__(self)
        self.set_name(con.login)
        self.set_con(con)


    def set_name(self, name):
        self.name = name


    def query_name(self):
        return self.name

    
    def set_con(self, con):
        self.con = con
        con.set_user_char(self)


    def query_con(self, con):
        return self.con


    def close_con(self):
        self.con.write("[Closing connection. Good bye.]\n")
        self.con.end_after_write()


    def con_closed(self):
        """Called by net.ConMan to tell us that the connection has been
        closed."""
        user_man = update_d.update_d.request_obj("sys.user_man",
                                                 "UserMan")
        user_man.end_user(self)


    def query_cap_name(self):
        return self.query_name().capitalize()


    def save(self):
        if not len(self.name):
            raise SaveErrorNoName
        file = open("user/%s" % self.query_name(), "wb")
        pickle.dump(self.props, file)
        file.close()
        print("[user] %s saved." % self.query_cap_name())


    def load(self):
        if not len(self.name):
            pass                # todo: do something interesting here

        file_name = "user/%s" % self.query_name()
        
        if os.path.exists(file_name):
            file = open("user/%s" % self.query_name(), "rb")
            self.props = pickle.load(file)
            file.close()

        return self

    
