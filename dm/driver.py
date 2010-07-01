#!/usr/bin/env python3
# main.py by Dannil
#
# This is the main source file for DannilMUD.
#

import sys

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
            import dm.sys.net   as net
            import dm.sys.login as login
            import dm.sys.user  as user
            print("done.")

            print("    Initializing user manager...     ", end = " ")
            user_man = user.UserMan()
            print("done.")

            print("    Initializing parser...           ", end = " ")
            parser = login.Parser(user_man, "cmds")
            print("done.")

            print("    Initializing network interface...", end = " ")
            con_man = net.ConMan(listen_port = 4851)
            print("done.")

            print("Boot sequence completed.")
            con_man.main_loop(parser.login_handler)


        except KeyboardInterrupt:
            print("Shutting down.")

        except:
            raise

driver = DannilMUD()
driver.boot()