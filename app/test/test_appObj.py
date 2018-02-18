#tests for appObj
from TestHelperSuperClass import testHelperSuperClass
from appObj import appObjClass, NotUTCException
import pytz
import datetime
import json

class test_appObjClass(testHelperSuperClass):
#Actual tests below

  def test_CreateAppOBjInstance(self):
    appObj = appObjClass()

  def test_InitialServerInfoMessage(self):
    appObj = appObjClass()
    #get now datetime.now(pytz.utc)
    curDatetime = pytz.timezone('UTC').localize(datetime.datetime(2018,1,1,13,46,0,0))
    serverInfo = appObj.getServerInfoJSON(curDatetime)
    expRes = json.dumps({'Server': {'ServerDatetime': str(curDatetime), 'DefaultUserTimezone': 'Europe/London'}, 'Jobs': {'TotalJobs': 0, 'NextExecuteJob': None}})
    self.assertJSONStringsEqual(json.dumps(serverInfo), expRes);

  def test_InitialServerInfoMessageOnlyAcceptsUTCTimezone(self):
    appObj = appObjClass()
    #get now datetime.now(pytz.utc)
    curDatetime = pytz.timezone('Europe/London').localize(datetime.datetime(2018,1,1,13,46,0,0))
    with self.assertRaises(Exception) as context:
      serverInfo = appObj.getServerInfoJSON(curDatetime)
    self.checkGotRightException(context,NotUTCException)


