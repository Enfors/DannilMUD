# login.py by Dannil - the login functions for DannilMUD

import os

import dm.daemon.update_d as update_d

class Parser:

    def __init__(self, user_man, cmds_dir):
        self.user_man = user_man
        self.login_state_funcs = { \
            "awaiting_login"  : self.login_state_awaiting_login,
            "awaiting_passwd" : self.login_state_awaiting_passwd,
            "idle"            : self.login_state_idle,

            "verify_create"   : self.login_state_verify_create,
            "create_passwd"   : self.login_state_create_passwd,
            "verify_passwd"   : self.login_state_verify_passwd
            #"awaiting_email"  : self.login_state_awaiting_email,
            }
        self._load_cmds(cmds_dir)

    #
    # Public functions
    #

    def login_handler(self, con, text):
        """Handle the login input from the user."""

        # Remove trailing white space.
        text = text.rstrip("\r\n\t ")
        
        #apply(self.login_state_funcs[con.login_state], (con, text))
        self.login_state_funcs[con.login_state](*(con, text))


    def parse_cmd(self, text):
        """Parse a user command.
Returns (cmd, (arg_list))."""
        words = text.split(" ")

        cmd = words[0]
        args = words[1:]

        return (cmd, args)
    

    #
    # Login state functions
    #

    def login_state_awaiting_login(self, con, text):
        con.login = text.lower()

        if len(text) < 2:
            con.num_failed_logins += 1
        elif os.path.exists("user/%s" % con.login):
            con.write("Password: ")
            con.login_state = "awaiting_passwd"
            return
        else:
            con.write("That user does not exist. " \
                      "Do you wish to create it?\nYes/no: ")
            con.login_state = "verify_create"
            return
        
        if con.num_failed_logins > 3:
            con.write("I grow tired of you. Good bye.\n")
            print("[login] User on fd %d from %s:%d failed to log in "
                  "too many times." % (con.fd, con.remote_ip, con.remote_port))
            con.end_after_write()
        else:
            con.write("Let's try this again. Login: ")
            

    def login_state_awaiting_passwd(self, con, text):
        entered_passwd = text
        user = self.user_man.init_user(con)

        if user.query("passwd") != text.strip():
            con.num_failed_logins += 1;
            con.write("Login incorrect. Please try again.\n\nLogin: ")
            con.login_state = "awaiting_login"
            return

        con.login_state = "idle"
        con.write("Welcome to DannilMUD, %s!\n> " % \
                  con.login.capitalize())
        print("[net] %s logged in." % user.query_cap_name())


    def login_state_idle(self, con, text):
        (cmd, args) = self.parse_cmd(text)
        
        cmd_parser = update_d.update_d.request_obj("sys.cmd_parser",
                                                   "CmdParser")
        cmd_parser.parse(text, con.query_user_char())
        
        con.write("> ")

        
    def login_state_verify_create(self, con, text):
        if text.lower() in ("y", "yes"):
            con.write("Ah, a new user. Please enter the password " \
                      "you wish to use.\nPassword: ")
            con.login_state = "create_passwd"
        else:
            con.write("Ok, log in with an existing user then.\nLogin: ")
            con.login_state = "awaiting_login"


    def login_state_create_passwd(self, con, text):
        if len(text) < 4:
            con.write("Your password has to be at least 4 " \
                      "characters long.\nPassword: ")
        else:
            con.passwd = text
            con.write("Please enter the same password again " \
                      "for verification.\nPassword: ")
            con.login_state = "verify_passwd"


    def login_state_verify_passwd(self, con, text):
        if text != con.passwd:
            con.write("The passwords do not match. Please try again.\n" \
                      "Password: ")
            con.login_state = "create_passwd"
        else:
            user = self.user_man.init_user(con)
            user.set("passwd", text)
            user.save()
            con.write("The passwords match. Thank you!\n> ")
            con.login_state = "idle"
            
    #
    # Internal functions
    #

    def _load_cmds(self, dir):
        self.cmds = os.listdir(dir)
