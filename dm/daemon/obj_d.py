# obj_d.py by Dannil

import dm.daemon.base_daemon as base_daemon

class ObjD(base_daemon.Daemon):
    def __init__(self):
        base_daemon.Daemon.__init__(self)

        self.objs = { }


    def register(self, obj):
        """Register an object with the object daemon.

        The object daemon will call obj.query_ref() which is expected
        to return a unique reference (identifyer). Subsequent calls
        to obj_d.request() with this reference will yield a Python
        object reference to obj in return."""

        ref = obj.query_ref()

        #print("[obj_d] Registering %s as %s." % (obj, ref))

        self.objs[ref] = obj


    def request(self, ref):
        """Return a Python reference to the specified object, or
        None if it's not registered."""
    
        if not ref in self.objs:
            #print("[obj_d] Object %s not found." % ref)
            return None
        else:
            #print("[obj_d] Returning %s for %s." % (self.objs[ref], ref))
            return self.objs[ref]

    
    def request_master(self, ref):
        return self.request(ref)


OBJ_D = ObjD()
        
