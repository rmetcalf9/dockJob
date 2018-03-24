from TestHelperSuperClass import testHelperAPIClient
import unittest
import json

data_simpleJobCreateParams = {
  "name": "TestJob",
  "repetitionInterval": "HOURLY:03",
  "command": "ls",
  "enabled": True
}

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
        'ServerStartupTime': '2018-01-01T13:46:00+00:00',
        'TotalJobExecutions': 0
      },
    }
    result = self.testClient.get('/api/serverinfo/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    resultJSON['Server']['ServerDatetime'] = 'IGNORE'
    self.assertJSONStringsEqual(resultJSON, expRes)

  def test_swaggerJSONProperlyShared(self):
    result = self.testClient.get('/api/swagger.json')
    self.assertEqual(result.status_code, 200)
    result = self.testClient.get('/apidocs/swagger.json')
    self.assertEqual(result.status_code, 200)

  def test_exectionCounter(self):
    expRes = {
      'Jobs': {
        'NextExecuteJob': '',
        'TotalJobs': 12
      },
      'Server': {
        'DefaultUserTimezone': 'Europe/London', 
        'ServerDatetime': 'IGNORE',
        'ServerStartupTime': '2018-01-01T13:46:00+00:00',
        'TotalJobExecutions': 4
      },
    }
    self.setupJobsAndExecutions(data_simpleJobCreateParams)
    result = self.testClient.get('/api/serverinfo/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    resultJSON['Server']['ServerDatetime'] = 'IGNORE'
    self.assertJSONStringsEqual(resultJSON, expRes)

