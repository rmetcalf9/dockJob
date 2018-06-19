from TestHelperSuperClass import testHelperAPIClient
import unittest
import json
from commonJSONStrings import data_simpleJobCreateParams, data_simpleJobCreateExpRes

class test_api(testHelperAPIClient):

  def test_getServerInfo(self):
    expRes = {
      'Jobs': {
        'NextJobsToExecute': [],
        'TotalJobs': 0,
        'JobsNeverRun': 0,
        'JobsCompletingSucessfully': 0,
        'JobsLastExecutionFailed': 0
      },
      'Server': {
        'DefaultUserTimezone': 'Europe/London', 
        'ServerDatetime': 'IGNORE',
        'ServerStartupTime': '2018-01-01T13:46:00+00:00',
        'TotalJobExecutions': 0,
        'MinutesBeforeMostRecentCompletionStatusBecomesUnknown': 49 * 60
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
    expResJobs = [data_simpleJobCreateExpRes]
    expRes = {
      'Jobs': {
        'NextJobsToExecute': expResJobs,
        'TotalJobs': 1,
        'JobsNeverRun': 1,
        'JobsCompletingSucessfully': 0,
        'JobsLastExecutionFailed': 0
      },
      'Server': {
        'DefaultUserTimezone': 'Europe/London', 
        'ServerDatetime': 'IGNORE',
        'ServerStartupTime': '2018-01-01T13:46:00+00:00',
        'TotalJobExecutions': 0,
        'MinutesBeforeMostRecentCompletionStatusBecomesUnknown': 49 * 60
      },
    }
    self.createJobs(1,data_simpleJobCreateParams)
    result = self.testClient.get('/api/serverinfo/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    resultJSON['Server']['ServerDatetime'] = 'IGNORE'
    resultJSON['Jobs']['NextJobsToExecute'][0]['guid'] = 'IGNORE'
    resultJSON['Jobs']['NextJobsToExecute'][0]['creationDate'] = 'IGNORE'
    resultJSON['Jobs']['NextJobsToExecute'][0]['lastUpdateDate'] = 'IGNORE'
    resultJSON['Jobs']['NextJobsToExecute'][0]['nextScheduledRun'] = 'IGNORE'
    expRes['Jobs']['NextJobsToExecute'][0]['name'] = data_simpleJobCreateExpRes['name'] + "001"
    self.assertJSONStringsEqual(resultJSON['Jobs']['NextJobsToExecute'], expRes['Jobs']['NextJobsToExecute'], msg='Next Job To execute detail mismatch') # Check just jobs first
    
    self.assertJSONStringsEqual(resultJSON, expRes, msg='Full comparison missmatch')


