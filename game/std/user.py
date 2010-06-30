# user.py by Dannil

import pickle

class User:
    def __init__(self, name):
        self.set_name(name)
        self.set_passwd(None)


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
        file = open("user/%s" % self.query_name(), "w")
        pickle.dump(self, file, 0)
        file.close()
        print "[user] %s saved." % self.query_cap_name()


    def load(self):
        pass
    

class UserMan:
    def __init__(self):
        self.users = {}


    def init_user(self, name):
        user = User(name)
        self.users[name] = user
        return user


    def query_user_exists(self, name):
        if os.path.exists("../data/user/%s" % name):
            return 1
        else:
            return 0


#    def __del__(self):
#        for user in self.users.values():
#            user.close() # Close the shelve
