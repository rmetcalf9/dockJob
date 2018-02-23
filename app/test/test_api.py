from TestHelperSuperClass import testHelperSuperClass
import unittest
from appObj import appObj
appObj.init()
import api
import json
from GlobalParamaters import GlobalParamaters, GlobalParamatersClass

env = {
  'APIAPP_MODE': 'DOCKER',
  'APIAPP_VERSION': 'TEST-3.3.3',
  'APIAPP_FRONTEND': '../app',
  'APIAPP_APIURL': 'http://apiurlxxx',
  'APIAPP_APIACCESSSECURITY': '[{ "type": "basic-auth" }]',
}


class test_api(testHelperSuperClass):
  testClient = None
  def setUp(self):
    GlobalParamaters.set(GlobalParamatersClass(env))
    self.testClient = appObj.flaskAppObject.test_client()
    self.testClient.testing = True 
  def tearDown(self):
    self.testClient = None

  def test_getServceInfo(self):
    expRes = json.dumps({
      'Jobs': {
        'NextExecuteJob': None,
        'TotalJobs': 0
      },
      'Server': {
        'DefaultUserTimezone': 'Europe/London', 
        'ServerDatetime': 'IGNORE'
      },
      })
    result = self.testClient.get('/api/serverinfo/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    resultJSON['Server']['ServerDatetime'] = 'IGNORE'
    self.assertJSONStringsEqual(resultJSON, json.loads(expRes));
    pass

