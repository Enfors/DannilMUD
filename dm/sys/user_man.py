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
            user.update()

        self.users[name] = user
        
        start_room = update_d.update_d.request_obj("obj.room",
                                                   "Room",
                                                   [ "obj.room",
                                                     "world/ooc/room",
                                                     [ 0, 0, 0 ] ] )
        start_room.load()
        start_room.recv_text("%s enters the game.\n" % name.capitalize())
        user.move_to_env(start_room)
        user.do_look()

        return user

    
    def end_user(self, user):
        del self.users[user.query_name()]
        
        #user.end()


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
