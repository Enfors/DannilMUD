# move_evt.py by Dannil

import dm.evt.action_evt as action_evt

class MoveEvt(action_evt.ActionEvt):
    pass

class LeaveEvt(MoveEvt):
    pass


class EnterEvt(MoveEvt):
    pass
