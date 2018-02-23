from TestHelperSuperClass import testHelperAPIClient
import unittest
from appObj import appObj
appObj.init()
import api
import json

class test_api(testHelperAPIClient):

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

  def test_swaggerJSONProperlyShared(self):
    result = self.testClient.get('/api/swagger.json')
    self.assertEqual(result.status_code, 200)
    result = self.testClient.get('/apidocs/swagger.json')
    self.assertEqual(result.status_code, 200)

