# living.py by Dannil

obj = __import__("obj")

class Living(obj.Obj):
    def __init__(self):
        set_name("unnamed")


    def set_name(self, name):
        self.name = name


    def query_name(self):
        return self.name
        