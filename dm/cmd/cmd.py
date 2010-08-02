# cmd.py by Dannil

class Cmd:
    def __init__(self):
        self.rules = [ ]


    def add_rule(self, rule):
        
        func_name = "rule_%s" % rule.replace(" ", "_")

        if not func_name in dir(self):
            print("Function missing for rule '%s'." % rule)
            return False

        self.rules.append(rule)
