# Logic for the monitorCheckTempState
import datetime
import pytz

MAX_NUMBERS_STORED = 10


class MonitorCheckTempState():
  credDict = None
  fns = None
  numberData = None

  def __init__(self, credDict, fns):
    # dict is none is not instalised
    self.credDict = credDict
    self.fns = fns
    self.resetData()

  def auth(self, username, password):
    if self.credDict is None:
      return False
    if self.credDict["username"] != username:
      return False
    if self.credDict["password"] != password:
      return False
    return True

  def resetData(self):
    self.numberData = {}

  def _deleteOldestUuid(self):
    keyList = list(self.numberData.keys())
    oldestKey = keyList[0]
    for key in keyList:
      if self.numberData[key]["dateSaved"] < self.numberData[oldestKey]["dateSaved"]:
        oldestKey=key
    del self.numberData[oldestKey]

  def storeNumber(self, uuidStr, number):
    if uuidStr not in self.numberData:
      if len(self.numberData) > 9:
        self._deleteOldestUuid()

    # This is a memory only data structure so no need to convert datetimes to iso format for storage
    self.numberData[uuidStr] = {
      "value": number,
      "dateSaved": datetime.datetime.now(pytz.timezone("UTC"))
    }
    return { "value": number }

  def getNumber(self, uuidStr):
    if uuidStr not in self.numberData:
      return None
    return {
      "value": self.numberData[uuidStr]["value"]
    }