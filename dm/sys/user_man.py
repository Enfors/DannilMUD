# user_man.py by Dannil

import os

import dm.obj.user_char as user_char

class UserMan:
    def __init__(self):
        self.users = {}


    def init_user(self, con):
        name = con.login
        user = user_char.UserChar(con)
        user = user.load()
        self.users[name] = user
        return user


    def end_user(self, user_char):
        del self.users[user_char.query_name()]


    def query_users(self):
        return self.users


    def query_user_exists(self, name):
        if os.path.exists("../data/user/%s" % name):
            return 1
        else:
            return 0


#    def __del__(self):
#        for user in self.users.values():
#            user.close() # Close the shelve
