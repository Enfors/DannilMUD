# user_char.py by Dannil

import os, pickle

import dm.obj.body as body

class UserChar(body.Body):
    def __init__(self, name):
        self.set_name(name)


    def set_name(self, name):
        self.name = name


    def query_name(self):
        return self.name

    
    def query_cap_name(self):
        return self.query_name().capitalize()


    def set_passwd(self, passwd):
        self.passwd = passwd


    def query_passwd(self):
        return self.passwd


    def save(self):
        if not len(self.name):
            raise SaveErrorNoName
        file = open("user/%s" % self.query_name(), "wb")
        #pickle.dump(self, file, 0)
        pickle.dump(self, file)
        file.close()
        print("[user] %s saved." % self.query_cap_name())


    def load(self):
        if not len(self.name):
            pass                # todo: do something interesting here

        file_name = "user/%s" % self.query_name()
        
        if os.path.exists(file_name):
            file = open("user/%s" % self.query_name(), "rb")
            obj = pickle.load(file)
            file.close()
            return obj
        else:
            return self

    
