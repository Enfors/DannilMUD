# pset.py by Dannil

import dm.cmd.wiz.wiz_cmd as wiz_cmd

class Cmd(wiz_cmd.WizCmd):
    def __init__(self):
        wiz_cmd.WizCmd.__init__(self)

        self.add_rule("pset here WORD STR")


    def rule_pset_here_WORD_STR(self, body, args):
        prop = args[0]
        val  = " ".join(args[1:])

        env = body.query_env()

        if not env:
            body.recv_tag_text("You have no environment to modify.\n")
            return False

        env.set(prop, val)
        body.recv_tag_text("Prop \"%s\" updated.\n" % prop)

