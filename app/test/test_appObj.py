#tests for appObj
from TestHelperSuperClass import testHelperAPIClient
from appObj import appObj, appObjClass, MissingUserForJobsException, MissingGroupForJobsException
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


  def test_missingUserForJobs(self):
    env = {
      'APIAPP_MODE': 'DOCKER',
      'APIAPP_VERSION': 'TEST-3.3.3',
      'APIAPP_FRONTEND': '../app',
      'APIAPP_APIURL': 'http://apiurlxxx:45/aa/bb/cc',
      'APIAPP_APIACCESSSECURITY': '[]',
      'APIAPP_GROUPFORJOBS': 'root',
    }
    with self.assertRaises(Exception) as context:
      appObj.init(env)
    self.checkGotRightException(context,MissingUserForJobsException)

  def test_missingUserForJobs(self):
    env = {
      'APIAPP_MODE': 'DOCKER',
      'APIAPP_VERSION': 'TEST-3.3.3',
      'APIAPP_FRONTEND': '../app',
      'APIAPP_APIURL': 'http://apiurlxxx:45/aa/bb/cc',
      'APIAPP_APIACCESSSECURITY': '[]',
      'APIAPP_USERFORJOBS': 'root',
    }
    with self.assertRaises(Exception) as context:
      appObj.init(env)
    self.checkGotRightException(context,MissingGroupForJobsException)

