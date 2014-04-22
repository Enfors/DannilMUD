# clone.py by Dannil

import dm.cmd.wiz.wiz_cmd as wiz_cmd

class Cmd(wiz_cmd.WizCmd):
    def setup(self):
        self.add_rule("clone PATH")


    def rule_clone_PATH(self, body, args):
        path = args[0]

        return self.clone(body, path)
    

    def clone(self, body, path):
        print("Path: ", path)
        mod = __import__("dm." + path.replace("/", "."))

        obj = eval("mod.%s.clone()" % path.replace("/", "."))

        body.recv_tag_text("Cloned %s.\n" % obj.query("short"))

        room = body.query_env()

        if not room:
            body.recv_tag_text("You don't have an environment.\n")
            obj.move_to_env(body)
        else:
            obj.move_to_env(room)
