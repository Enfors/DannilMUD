#!/usr/bin/env python3
# main.py by Dannil
#
# This is the main source file for DannilMUD.
#

import sys

import dm.daemon.update_d as update_d

class DannilMUD:
    def __init__(self):
        pass


    def boot(self):

        print("")
        print("  +-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
        print("  |                                                         |")
        print("  | DannilMUD (C) Christer Enfors A.K.A. Dannil 2007 - 2010 |")
        print("  |                                                         |")
        print("  +-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
        print("")
        
        try:
            print("Commencing boot sequence.")

            print("    Importing modules...             ", end = " ")
            import dm.daemon.update_d as update_d
            import dm.sys.net         as net
            import dm.sys.login       as login
            import dm.sys.user_man    as user_man
            print("done.")

            print("    Initializing user manager...     ", end = " ")
            self.user_man = user_man.UserMan()
            print("done.")

            print("    Initializing parser...           ", end = " ")
            self.parser = login.Parser(self.user_man, "cmd")
            print("done.")

            print("    Initializing network interface...", end = " ")
            self.con_man = net.ConMan(listen_port = 4851)
            print("done.")

            print("Boot sequence completed.")
            #con_man.main_loop(parser.login_handler)
            self.main_loop()

        except KeyboardInterrupt:
            print("Shutting down.")

        except:
            raise

    def main_loop(self):
        while True:
            self.con_man.handle_one_event(self.parser.login_handler)


driver = DannilMUD()
driver.boot()
