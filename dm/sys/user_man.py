# user_man.py by Dannil

import os

import dm.daemon.update_d as update_d
import dm.obj.user_char   as user_char

class UserMan:
    def __init__(self):
        self.users = {}


    def init_user(self, con, new_user = False):
        name = con.login
        user = user_char.UserChar(con)

        if new_user:
            user.set("short", name.capitalize())
        else:
            user = user.load()


        self.users[name] = user
        
        lobby = update_d.update_d.request_obj("sys.lobby", "Lobby")
        user.move_to_env(lobby)

        return user


    def end_user(self, user):
        del self.users[user.query_name()]
        
        if user.env:
            user.env.remove_contents(user)


    def query_users(self):
        return self.users


    def query_user_exists(self, name):
        if os.path.exists("../data/user/%s" % name):
            return 1
        else:
            return 0


    def query_user_online(self, name):
        return name in self.users.keys()

#    def __del__(self):
#        for user in self.users.values():
#            user.close() # Close the shelve
