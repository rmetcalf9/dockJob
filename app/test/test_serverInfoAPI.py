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
        'HoursBeforeMostRecentCompletionStatusBecomesUnknown': 49
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
    expResJobs = [{
      'name': 'TestJob001',
      'command': 'ls',
      'enabled': True,
      'guid': 'IGNORE',
      'creationDate': 'IGNORE',
      'lastRunDate': 'IGNORE',
      'lastUpdateDate': 'IGNORE',
      'nextScheduledRun': 'IGNORE',
      'repetitionInterval': 'HOURLY:03',
      'lastRunExecutionGUID': '',
      'lastRunReturnCode': None,
      'mostRecentCompletionStatus': 'Unknown',
      'pinned': False
    }]
    #   {"Jobs": {"NextJobsToExecute": [{"command": "ls", "creationDate": "2018-03-24T18:20:12.444284+00:00", "enabled": true, "": "e668fafb-af66-4ac7-8a5a-7ba080d1e287", "lastRunDate": null, "lastUpdateDate": "2018-03-24T18:20:12.444284+00:00", "name": "TestJob001", "nextScheduledRun": "2018-03-24T19:03:00+00:00", "repetitionInterval": "HOURLY:03"}], "TotalJobs": 1}, "Server": {"DefaultUserTimezone": "Europe/London", "ServerDatetime": "IGNORE", "ServerStartupTime": "2018-01-01T13:46:00+00:00", "TotalJobExecutions": 0}
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
        'HoursBeforeMostRecentCompletionStatusBecomesUnknown': 49
      },
    }
    self.createJobs(1,data_simpleJobCreateParams)
    result = self.testClient.get('/api/serverinfo/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    resultJSON['Server']['ServerDatetime'] = 'IGNORE'
    resultJSON['Jobs']['NextJobsToExecute'][0]['guid'] = 'IGNORE'
    resultJSON['Jobs']['NextJobsToExecute'][0]['creationDate'] = 'IGNORE'
    resultJSON['Jobs']['NextJobsToExecute'][0]['lastRunDate'] = 'IGNORE'
    resultJSON['Jobs']['NextJobsToExecute'][0]['lastUpdateDate'] = 'IGNORE'
    resultJSON['Jobs']['NextJobsToExecute'][0]['nextScheduledRun'] = 'IGNORE'
    self.assertJSONStringsEqual(resultJSON, expRes)


