# light_source.py by Dannil

import dm.obj.base as base

class LightSource(base.Base):
    def __init__(self):
        base.Base.__init__(self)

        self.set("light_source", 10)
