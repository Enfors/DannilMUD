class Error(Exception):
    def __init__(self, text = None):
        self.text = text


    def __str__(self):
        return self.text


class InternalError(Error):
    pass


class BuildingError(Error):
    pass


class CmdFailed(Error):
    pass
