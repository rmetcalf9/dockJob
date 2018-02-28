#tests for appObj
from TestHelperSuperClass import testHelperAPIClient
from appObj import appObj, appObjClass
import pytz
import datetime
import json

class test_appObjClass(testHelperAPIClient):
#Actual tests below

  def test_CreateAppOBjInstance(self):
    pass

  def test_InitialServerInfoMessage(self):
    #get now datetime.now(pytz.utc)
    curDatetime = pytz.timezone('UTC').localize(datetime.datetime(2018,1,1,13,46,0,0))
    serverInfo = appObj.getServerInfoJSON(curDatetime)
    expRes = json.dumps({'Server': {'ServerDatetime': curDatetime.isoformat(), 'DefaultUserTimezone': 'Europe/London'}, 'Jobs': {'TotalJobs': 0, 'NextExecuteJob': None}})
    self.assertJSONStringsEqual(json.dumps(serverInfo), expRes);

  def test_InitialServerInfoMessageOnlyAcceptsUTCTimezone(self):
    #get now datetime.now(pytz.utc)
    curDatetime = pytz.timezone('Europe/London').localize(datetime.datetime(2018,1,1,13,46,0,0))
    with self.assertRaises(Exception) as context:
      serverInfo = appObj.getServerInfoJSON(curDatetime)
    self.checkGotRightException(context,appObjClass.NotUTCException)


