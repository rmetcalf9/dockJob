from TestHelperSuperClass import testHelperAPIClient
import unittest
import json

class test_api(testHelperAPIClient):

  def test_getServceInfo(self):
    expRes = {
      'Jobs': {
        'NextExecuteJob': '',
        'TotalJobs': 0
      },
      'Server': {
        'DefaultUserTimezone': 'Europe/London', 
        'ServerDatetime': 'IGNORE',
        'ServerStartupTime': '2018-01-01T13:46:00+00:00'
      },
    }
    result = self.testClient.get('/api/serverinfo/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    resultJSON['Server']['ServerDatetime'] = 'IGNORE'
    self.assertJSONStringsEqual(resultJSON, expRes)
    pass

  def test_swaggerJSONProperlyShared(self):
    result = self.testClient.get('/api/swagger.json')
    self.assertEqual(result.status_code, 200)
    result = self.testClient.get('/apidocs/swagger.json')
    self.assertEqual(result.status_code, 200)

