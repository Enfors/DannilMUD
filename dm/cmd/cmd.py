# cmd.py by Dannil

class Cmd:
    def __init__(self):
        self.rules = [ ]

        self.setup()

    
    def setup(self):
        pass


    def add_rule(self, rule):
        rule = rule.split()
        func_name = "rule_" + "_".join(rule)
        #func_name = "rule_%s" % rule.replace(" ", "_")

        if not func_name in dir(self):
            print("Function missing for rule '%s'." % rule)
            return False

        self.rules.append(rule)
