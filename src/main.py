#!/usr/bin/env python
# main.py by Dannil
#
# This is the main source file for DannilMUD.
#

import sys
sys.path.insert(0, "std")

class DannilMUD:
    def __init__(self):
        pass


    def boot(self):
        print
        print "    +--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--+"
        print "    |                                                  |"
        print "    | DannilMUD (C) Christer Enfors A.K.A. Dannil 2007 |"
        print "    |                                                  |"
        print "    +--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--+"
        print
        
        try:
            print "Commencing boot sequence."

            print "    Importing modules...             ",
            net  = __import__("net")
            io   = __import__("io")
            user = __import__("user")
            print "done."

            print "    Initializing user manager...     ",
            user_man = user.UserMan()
            print "done."

            print "    Initializing parser...           ",
            parser = io.Parser(user_man, "cmds")
            print "done."

            print "    Initializing network interface...",
            con_man = net.ConMan(listen_port = 4851)
            print "done."

            print "Boot sequence completed."
            con_man.main_loop(parser.login_handler)


        except KeyboardInterrupt:
            print "Shutting down."

        except:
            raise

driver = DannilMUD()
driver.boot()
