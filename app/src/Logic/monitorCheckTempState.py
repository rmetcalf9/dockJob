# Logic for the monitorCheckTempState

MAX_NUMBERS_STORED = 10


class MonitorCheckTempState():
  credDict = None
  fns = None

  def __init__(self, credDict, fns):
    # dict is none is not instalised
    self.credDict = credDict
    self.fns = fns

  def auth(self, username, password):
    if self.credDict is None:
      return False
    if self.credDict["username"] != username:
      return False
    if self.credDict["password"] != password:
      return False
    return True