# update_d.py by Dannil

import imp, sys

import dm.daemon.base_daemon as base_daemon

class UpdateD(base_daemon.Daemon):
    def __init__(self):
        base_daemon.Daemon.__init__(self)
        self.modules = { }
        self.objects = { }


    def request_obj(self, module_path, class_name, args = None):
        # Remove trailing .py, if present
        if module_path[-3:] == ".py":
            module_path = module_path[:-3]

        # Check if the module has been loaded.
        if not module_path in self.modules:
            # todo: handle exceptions here

            # The module hasn't been loaded yet. Load it now.
            mod = __import__("dm." + module_path)

            self.modules[module_path] = mod
            self.objects[module_path] = { }
        else:
            # Module already loaded. Retreive it from cache.
            mod = self.modules[module_path]

        # Check if the object is loaded.
        if not class_name in self.objects[module_path]:
            # The object is not loaded. Load it now.

            if args:
                class_path = "mod.%s.%s(args)" % (module_path, class_name)
            else:
                class_path = "mod.%s.%s()"     % (module_path, class_name)

            self.objects[module_path][class_name] = eval(class_path)

        return self.objects[module_path][class_name]


    def reload_module(self, module_path):
        print("[update_d] Reloading %s." % module_path)

        if not module_path in self.modules:
            print("[update_d] Module not loaded.\n")
            print("Modules: %s\n" % self.modules)
            return False

        imp.reload(sys.modules["dm.%s" % module_path])

        self.objects[module_path] = { }

        return True


update_d = UpdateD()
