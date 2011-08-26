# reload.py by Dannil

import dm.cmd.wiz.wiz_cmd as wiz_cmd

import dm.daemon.update_d as update_d

class Cmd(wiz_cmd.WizCmd):
    def __init__(self):
        wiz_cmd.WizCmd.__init__(self)

        self.add_rule("reload")
        self.add_rule("reload STR")


    def rule_reload(self, user, args):
        user.recv_text("What do you want to reload?\n")


    def rule_reload_STR(self, user, args):
        if update_d.update_d.reload_module(args[0]):
            user.recv_text("Done.\n")
        else:
            user.recv_text("Operation failed.\n")

