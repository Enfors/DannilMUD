# pquery.py by Dannil

import dm.cmd.wiz.wiz_cmd as wiz_cmd

class Cmd(wiz_cmd.WizCmd):
    def __init__(self):
        wiz_cmd.WizCmd.__init__(self)

        self.add_rule("pquery here WORD")


    def rule_pquery_here_WORD(self, body, args):
        prop = args[0]

        env = body.query_env()

        if not env:
            body.recv_tag_text("You have no environment to query.\n")
            
        indent = 9 + len(prop)

        body.recv_tag_text("Prop \"%s\": %s\n" % (prop,
                                                  str(env.query(prop))),
                           indent2 = indent)
