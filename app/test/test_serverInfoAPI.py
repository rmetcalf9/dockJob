from TestHelperSuperClass import testHelperAPIClient
import unittest
import json
from commonJSONStrings import data_simpleJobCreateParams, data_simpleJobCreateExpRes, data_simpleManualJobCreateParams

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

  def getNextJobToExecuteGUID(self):
    serverInfoAPIresult = self.testClient.get('/api/serverinfo/')
    self.assertEqual(serverInfoAPIresult.status_code, 200)
    serverInfoAPIresultJSON = json.loads(serverInfoAPIresult.get_data(as_text=True))
    if (len(serverInfoAPIresultJSON["Jobs"]["NextJobsToExecute"]) == 0):
      return None
    if (len(serverInfoAPIresultJSON["Jobs"]["NextJobsToExecute"]) == 1):
      return serverInfoAPIresultJSON["Jobs"]["NextJobsToExecute"][0]["guid"]
    raise Exception("Mutiple next job case not catered for in test")


  def test_changeJobFromUnschdeuledToScheduledAppearsAsNExtJobToRun(self):
    # Issue #69 found a bug where if I create a job that is not scheduled and switch it to scheduled it was not appearing in the next job to run form.
    jobParams = dict(data_simpleManualJobCreateParams)
    param = self.createJobs(1,jobParams)
    jobGUID = param[0]["createResult"]["guid"]
    self.assertEqual(self.getNextJobToExecuteGUID(), None)

    jobParams["repetitionInterval"] = data_simpleJobCreateParams["repetitionInterval"]
    jobParams["enabled"] = data_simpleJobCreateParams["enabled"]
    updateJobResult = self.testClient.put('/api/jobs/' + jobGUID, data=json.dumps(jobParams), content_type='application/json')
    self.assertEqual(updateJobResult.status_code, 200)
    #Now the job has been created but then later set to scheduled it should be in the server API result as the next job to be scheduled
    self.assertEqual(self.getNextJobToExecuteGUID(), jobGUID)

  def test_enableAndDisableRecaculatesNExtJobToExecute(self):
    #Create a job that is scheduled
    #Update that job so it is not scheduled
    #Check there is no job in next job to execute
    #Update that job so it is enabled
    #Check it is now enabled again
    jobParams = dict(data_simpleJobCreateParams)
    param = self.createJobs(1,jobParams)
    jobGUID = param[0]["createResult"]["guid"]
    self.assertEqual(self.getNextJobToExecuteGUID(), jobGUID)

    jobParams["enabled"] = data_simpleManualJobCreateParams["enabled"]
    updateJobResult = self.testClient.put('/api/jobs/' + jobGUID, data=json.dumps(jobParams), content_type='application/json')
    self.assertEqual(updateJobResult.status_code, 200)
    self.assertEqual(self.getNextJobToExecuteGUID(), None, msg="Disabled job but it still reports to be scheduled")

    jobParams["enabled"] = data_simpleJobCreateParams["enabled"]
    updateJobResult = self.testClient.put('/api/jobs/' + jobGUID, data=json.dumps(jobParams), content_type='application/json')
    self.assertEqual(updateJobResult.status_code, 200)
    self.assertEqual(self.getNextJobToExecuteGUID(), jobGUID, msg="Reenabled job but it still reports to be scheduled")


