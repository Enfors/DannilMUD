# update_d.py by Dannil

import dm.daemon.daemon as daemon

class UpdateD(daemon.Daemon):
    def __init__(self):
        self.modules = { }
        self.objects = { }


    def request_obj(self, module_path, class_name):
        # Remove trailing .py, if present
        if module_path[-3:] == ".py":
            module_path = module_path[:-3]

        if not module_path in self.modules:
            # todo: handle exceptions here

            # The module hasn't been loaded yet. Load it now.

            m = __import__("dm." + module_path)

            self.modules[module_path] = m
            self.objects[module_path] = { }

        if not class_name in self.objects[module_path]:
            # The object is not loaded. Load it now.

            class_path = "m.%s.%s()" % (module_path, class_name)

            self.objects[module_path][class_name] = eval(class_path)

        return self.objects[module_path][class_name]



update_d = UpdateD()
