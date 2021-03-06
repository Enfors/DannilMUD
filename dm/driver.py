#!/usr/bin/env python3
# main.py by Dannil
#
# This is the main source file for DannilMUD.
#

import sys, traceback

import dm.daemon.update_d as update_d

class DannilMUD:
    def __init__(self):
        pass


    def boot(self):

        print("")
        print("  +-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
        print("  |                                                         |")
        print("  | DannilMUD (C) Christer Enfors A.K.A. Dannil 2007 - 2014 |")
        print("  |                                                         |")
        print("  +-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
        print("")
        
        try:
            print("Commencing boot sequence.")

            print("    Importing modules...             ", end = " ")
            import dm.daemon.update_d as update_d
            import dm.sys.net         as net
            import dm.sys.login       as login
            print("done.")

            print("    Initializing user manager...     ", end = " ")
            self.user_man = update_d.update_d.request_obj("sys.user_man",
                                                          "UserMan")
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
            try:
                self.con_man.handle_one_event(self.parser.login_handler)
            except KeyboardInterrupt:
                raise
            except:
                t, v, b = sys.exc_info()
                traceback.print_exception(t, v, b)


driver = DannilMUD()
driver.boot()
