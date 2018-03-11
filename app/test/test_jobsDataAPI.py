from TestHelperSuperClass import testHelperAPIClient

import json
from utils import from_iso8601

data_simpleJobCreateParams = {
  "name": "TestJob",
  "repetitionInterval": "HOURLY:03",
  "command": "ls",
  "enabled": True
}
data_simpleJobCreateExpRes = {
  "guid": 'IGNORE', 
  "name": data_simpleJobCreateParams['name'], 
  "command": data_simpleJobCreateParams['command'], 
  "enabled": data_simpleJobCreateParams['enabled'], 
  "repetitionInterval": data_simpleJobCreateParams['repetitionInterval'], 
  "nextScheduledRun": 'IGNORE', 
  "creationDate": "IGNORE", 
  "lastUpdateDate": "IGNORE",
  "lastRunDate": None,
}
data_simpleJobExecutionCreateExpRes = {
  "guid": 'IGNORE',
  "stage": 'Pending', 
  "executionName": 'TestExecutionName', 
  "resultReturnCode": 0, 
  "jobGUID": 'OVERRIDE',
  "jobCommand": 'OVERRIDE',
  "resultsSTDOUT": '', 
  "manual": True, 
  "dateCreated": 'IGNORE', 
  "dateStarted": 'IGNORE', 
  "dateCompleted": 'IGNORE' 
}

class test_jobsData(testHelperAPIClient):
  def assertJSONJobStringsEqual(self, result,expectedResult):
    #ignores fields that may be different
    result['guid'] = expectedResult['guid']
    result['nextScheduledRun'] = expectedResult['nextScheduledRun']
    result['creationDate'] = expectedResult['creationDate']
    result['lastUpdateDate'] = expectedResult['lastUpdateDate']
    self.assertJSONStringsEqual(result, expectedResult);

  def getTotalJobs(self):
    result2 = self.testClient.get('/api/serverinfo/')
    self.assertEqual(result2.status_code, 200)
    resultJSON = json.loads(result2.get_data(as_text=True))
    return resultJSON['Jobs']['TotalJobs']
    
  def assertCorrectTotalJobs(self, num):
    # Ensure total reflected in serverinfo
    self.assertEqual(self.getTotalJobs(), num, msg='Server Info Total Jobs field not correct');

  def test_JobCreate(self):
    result = self.testClient.post('/api/jobs/', data=json.dumps(data_simpleJobCreateParams), content_type='application/json')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertEqual(len(resultJSON['guid']), 36, msg='Invalid GUID - must be 36 chars')
    self.assertEqual(resultJSON['creationDate'], resultJSON['lastUpdateDate'], msg='Creation date dosen''t match last update')
    tim = from_iso8601(resultJSON['creationDate'])
    self.assertTimeCloseToCurrent(tim)
    self.assertJSONJobStringsEqual(resultJSON, data_simpleJobCreateExpRes)
    self.assertCorrectTotalJobs(1)

  def test_JobCreateDuplicateErrors(self):
    result = self.testClient.post('/api/jobs/', data=json.dumps(data_simpleJobCreateParams), content_type='application/json')
    self.assertEqual(result.status_code, 200, msg='First job creation should have worked')
    result = self.testClient.post('/api/jobs/', data=json.dumps(data_simpleJobCreateParams), content_type='application/json')
    self.assertEqual(result.status_code, 400, msg='Duplicate job creation didn''t return 400')

  def test_JobCreateBadValidation(self):
    params = {
      "name": "TestJob",
      "repetitionInterval": "INVALIDREPINT:03",
      "command": "ls",
      "enabled": True
    }
    result = self.testClient.post('/api/jobs/', data=json.dumps(params), content_type='application/json')
    self.assertEqual(result.status_code, 400, msg='Badly formatted job didn''t  return 400')

  def test_JobCreateBlankRepititionInterval(self):
    params = {
      "name": "TestJob",
      "repetitionInterval": None,
      "command": "ls",
      "enabled": True
    }
    result = self.testClient.post('/api/jobs/', data=json.dumps(params), content_type='application/json')
    self.assertEqual(result.status_code, 400, msg='Blank repitition was accepted (Use empty string)')

  def test_JobCreateEmptyRepititionInterval(self):
    params = {
      "name": "TestJob",
      "repetitionInterval": '',
      "command": "ls",
      "enabled": True
    }
    result = self.testClient.post('/api/jobs/', data=json.dumps(params), content_type='application/json')
    self.assertEqual(result.status_code, 200, msg='Empty repitition interval not accepted')

  def test_jobCreateAndQueryBackByGUID(self):
    result = self.testClient.post('/api/jobs/', data=json.dumps(data_simpleJobCreateParams), content_type='application/json')
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertEqual(result.status_code, 200, msg='First job creation should have worked')
    result2 = self.testClient.get('/api/jobs/' + resultJSON['guid'])
    self.assertEqual(result2.status_code, 200, msg='Read back record')
    result2JSON = json.loads(result2.get_data(as_text=True))
    self.assertJSONJobStringsEqual(resultJSON, data_simpleJobCreateExpRes);

  def test_jobGetInvalid(self):
    result = self.testClient.get('/api/jobs/INVALID_KEY')
    self.assertEqual(result.status_code, 400, msg='Didn''t return not found job')

  def test_jobCreateAndQueryBackByName(self):
    result = self.testClient.post('/api/jobs/', data=json.dumps(data_simpleJobCreateParams), content_type='application/json')
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertEqual(result.status_code, 200, msg='First job creation should have worked')
    result2 = self.testClient.get('/api/jobs/' + resultJSON['name'])
    self.assertEqual(result2.status_code, 200, msg='Read back record')
    result2JSON = json.loads(result2.get_data(as_text=True))
    self.assertJSONJobStringsEqual(resultJSON, data_simpleJobCreateExpRes);

  def findRecord(self, params, name):
    for cur in params:
      if (name==params[cur]['name']):
        return params[cur]
    return None

  def createJobs(self, num, basis):
    jobsAtStart = self.getTotalJobs()
    param = {}
    for cur in range(0, num):
      param[cur] = dict(basis)
      param[cur]['name'] = basis['name'] + str(cur+1).zfill(3)
      result = self.testClient.post('/api/jobs/', data=json.dumps(param[cur]), content_type='application/json')
      self.assertEqual(result.status_code, 200, msg='job creation failed')
    self.assertCorrectTotalJobs(num + jobsAtStart)
    return param

  def test_jobCreateAndQueryBackByName(self):
    numTestRecords = 6
    param = self.createJobs(numTestRecords, data_simpleJobCreateParams)
    result2 = self.testClient.get('/api/jobs/')
    self.assertEqual(result2.status_code, 200, msg='Fetch failed')
    result2JSON = json.loads(result2.get_data(as_text=True))
    expPaginationResult = {'offset': 0, 'pagesize': 20, 'total': numTestRecords}
    self.assertJSONStringsEqual(result2JSON["pagination"], expPaginationResult);
    self.assertEqual(len(result2JSON["result"]),numTestRecords,msg="Wrong number of returned results")
    exp = dict(data_simpleJobCreateExpRes)
    for cur in range(0,numTestRecords):
      thisParam = self.findRecord(param, result2JSON["result"][cur]['name'])
      exp['name'] = thisParam['name']
      self.assertJSONJobStringsEqual(result2JSON["result"][cur], exp)

  def test_jobQueryPaginationTests(self):
    exp = dict(data_simpleJobCreateExpRes)
    numTestRecords = 45
    pagesize = 15
    param = self.createJobs(numTestRecords, data_simpleJobCreateParams)

    #Query back first page of 15
    result2 = self.testClient.get('/api/jobs/?pagesize=' + str(pagesize))
    self.assertEqual(result2.status_code, 200, msg='Fetch failed')
    result2JSON = json.loads(result2.get_data(as_text=True))
    expPaginationResult = {'offset': 0, 'pagesize': pagesize, 'total': numTestRecords}
    self.assertJSONStringsEqual(result2JSON["pagination"], expPaginationResult);
    self.assertEqual(len(result2JSON["result"]),pagesize,msg="Wrong number of returned results in first page")
    for cur in range(0,pagesize):
      exp['name'] = param[cur]['name']
      self.assertJSONJobStringsEqual(result2JSON["result"][cur], exp);

    #Query back 2nd page of 15
    offset = 15
    result2 = self.testClient.get('/api/jobs/?pagesize=' + str(pagesize) + '&offset=' + str(offset))
    self.assertEqual(result2.status_code, 200, msg='Fetch failed')
    result2JSON = json.loads(result2.get_data(as_text=True))
    expPaginationResult = {'offset': offset, 'pagesize': pagesize, 'total': numTestRecords}
    self.assertJSONStringsEqual(result2JSON["pagination"], expPaginationResult);
    self.assertEqual(len(result2JSON["result"]),pagesize,msg="Wrong number of returned results in second page")
    for cur in range(0,pagesize):
      exp['name'] = param[cur + offset]['name']
      self.assertJSONJobStringsEqual(result2JSON["result"][cur], exp);

    #Query back 3rd final page (only 5 left)
    offset = 30
    result2 = self.testClient.get('/api/jobs/?pagesize=' + str(pagesize) + '&offset=' + str(offset))
    self.assertEqual(result2.status_code, 200, msg='Fetch failed')
    result2JSON = json.loads(result2.get_data(as_text=True))
    expPaginationResult = {'offset': offset, 'pagesize': pagesize, 'total': numTestRecords}
    self.assertJSONStringsEqual(result2JSON["pagination"], expPaginationResult);
    self.assertEqual(len(result2JSON["result"]),pagesize,msg="Wrong number of returned results in last page")
    for cur in range(0,numTestRecords - offset):
      exp['name'] = param[cur + offset]['name']
      self.assertJSONJobStringsEqual(result2JSON["result"][cur], exp);

  def test_jobDeleteByGUID(self):
    backgroundData = dict(data_simpleJobCreateParams)
    backgroundData['name'] = 'BackgroundData'
    self.createJobs(10, data_simpleJobCreateParams)
    result = self.testClient.post('/api/jobs/', data=json.dumps(data_simpleJobCreateParams), content_type='application/json')
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertEqual(result.status_code, 200, msg='First job creation should have worked')
    result2 = self.testClient.delete('/api/jobs/' + resultJSON['guid'])
    self.assertEqual(result2.status_code, 200, msg='Didn''t delete record')
    result2JSON = json.loads(result2.get_data(as_text=True))
    self.assertJSONJobStringsEqual(result2JSON, data_simpleJobCreateExpRes);
    result3 = self.testClient.get('/api/jobs/' + resultJSON['name'])
    self.assertEqual(result3.status_code, 400, msg='Managed to retrieve deleted job by name')
    result4 = self.testClient.get('/api/jobs/' + resultJSON['guid'])
    self.assertEqual(result4.status_code, 400, msg='Managed to retrieve deleted job by guid')
    self.assertCorrectTotalJobs(10)

  def test_jobDeleteByName(self):
    result = self.testClient.post('/api/jobs/', data=json.dumps(data_simpleJobCreateParams), content_type='application/json')
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertEqual(result.status_code, 200, msg='First job creation should have worked')
    guid_of_job_to_be_deleted = resultJSON['guid']
    name_of_job_to_be_deleted = resultJSON['name']
    # create a second job which won't be deleted
    p2 = dict(data_simpleJobCreateParams)
    p2['name'] = 'JobNotToBeDeleted'
    result = self.testClient.post('/api/jobs/', data=json.dumps(p2), content_type='application/json')
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertEqual(result.status_code, 200, msg='Second job creation should have worked')

    #Delete record by name
    delete_result = self.testClient.delete('/api/jobs/' + name_of_job_to_be_deleted)
    self.assertEqual(delete_result.status_code, 200, msg='Didn''t delete record')
    delete_resultJSON = json.loads(delete_result.get_data(as_text=True))
    self.assertJSONJobStringsEqual(delete_resultJSON, data_simpleJobCreateExpRes);

    #Further checks
    result3 = self.testClient.get('/api/jobs/' + name_of_job_to_be_deleted)
    self.assertEqual(result3.status_code, 400, msg='Managed to retrieve deleted job by name')
    result4 = self.testClient.get('/api/jobs/' + guid_of_job_to_be_deleted)
    self.assertEqual(result4.status_code, 400, msg='Managed to retrieve deleted job by guid')
    self.assertCorrectTotalJobs(1)

  def test_jobDeleteByGUIDNotExist(self):
    result2 = self.testClient.delete('/api/jobs/' + 'BAD-GUID-OR-NAME')
    self.assertEqual(result2.status_code, 400, msg='Deleted a record')
    self.assertCorrectTotalJobs(0)

  def test_jobFilter(self):
    numShown = 3
    exp = dict(data_simpleJobCreateExpRes)
    p1 = dict(data_simpleJobCreateParams)
    p1['name'] = 'NotIntrested'
    p2 = dict(data_simpleJobCreateParams)
    p2['name'] = 'ShowInFilterPrr'
    p3 = dict(data_simpleJobCreateParams)
    p3['name'] = 'HideAway'
    param1 = self.createJobs(6, p1)
    param2 = self.createJobs(numShown, p2)
    param3 = self.createJobs(8, p3)
    
    #Now query back only our showed records
    # using simple non-paginated query
    result2 = self.testClient.get('/api/jobs/?query=Prr')
    self.assertEqual(result2.status_code, 200, msg='Fetch failed')
    result2JSON = json.loads(result2.get_data(as_text=True))
    expPaginationResult = {'offset': 0, 'pagesize': 20, 'total': numShown}
    self.assertJSONStringsEqual(result2JSON["pagination"], expPaginationResult);
    for cur in range(0,numShown):
      exp['name'] = param2[cur]['name']
      self.assertJSONJobStringsEqual(result2JSON["result"][cur], exp);

  def test_jobFilterCommand(self):
    numShown = 3
    exp = dict(data_simpleJobCreateExpRes)
    p1 = dict(data_simpleJobCreateParams)
    p1['name'] = 'NotIntrested'
    p2 = dict(data_simpleJobCreateParams)
    p2['name'] = 'ShowInFilterPrr'
    p2['command'] = 'xxxfeEdComm'
    p3 = dict(data_simpleJobCreateParams)
    p3['name'] = 'HideAway'
    param1 = self.createJobs(6, p1)
    param2 = self.createJobs(numShown, p2)
    param3 = self.createJobs(8, p3)
    
    #Now query back only our showed records
    # using simple non-paginated query
    result2 = self.testClient.get('/api/jobs/?query=FEed')
    self.assertEqual(result2.status_code, 200, msg='Fetch failed')
    result2JSON = json.loads(result2.get_data(as_text=True))
    expPaginationResult = {'offset': 0, 'pagesize': 20, 'total': numShown}
    self.assertJSONStringsEqual(result2JSON["pagination"], expPaginationResult);
    for cur in range(0,numShown):
      exp['name'] = param2[cur]['name']
      exp['command'] = param2[cur]['command']
      self.assertJSONJobStringsEqual(result2JSON["result"][cur], exp);

  def test_jobFilterTwoClausesPositive(self):
    numShown = 3
    exp = dict(data_simpleJobCreateExpRes)
    p1 = dict(data_simpleJobCreateParams)
    p1['name'] = 'NotIntrested'
    p2 = dict(data_simpleJobCreateParams)
    p2['name'] = 'ShowInFilterPrr'
    p3 = dict(data_simpleJobCreateParams)
    p3['name'] = 'HideAway'
    param1 = self.createJobs(6, p1)
    param2 = self.createJobs(numShown, p2)
    param3 = self.createJobs(8, p3)
    
    #Now query back only our showed records
    # using simple non-paginated query
    result2 = self.testClient.get('/api/jobs/?query=in%20filt')
    self.assertEqual(result2.status_code, 200, msg='Fetch failed')
    result2JSON = json.loads(result2.get_data(as_text=True))
    expPaginationResult = {'offset': 0, 'pagesize': 20, 'total': numShown}
    self.assertJSONStringsEqual(result2JSON["pagination"], expPaginationResult);
    for cur in range(0,numShown):
      exp['name'] = param2[cur]['name']
      self.assertJSONJobStringsEqual(result2JSON["result"][cur], exp);

  def test_jobFilterTwoClausesNegative(self):
    numNotShown = 3
    exp = dict(data_simpleJobCreateExpRes)
    p1 = dict(data_simpleJobCreateParams)
    p1['name'] = 'NotIntrested'
    p2 = dict(data_simpleJobCreateParams)
    p2['name'] = 'ShowInFilterPrr'
    p3 = dict(data_simpleJobCreateParams)
    p3['name'] = 'HideAway'
    param1 = self.createJobs(6, p1)
    param2 = self.createJobs(numNotShown, p2)
    param3 = self.createJobs(8, p3)
    
    #Now query back only our showed records
    # using simple non-paginated query
    result2 = self.testClient.get('/api/jobs/?query=in%20fiiilt')
    self.assertEqual(result2.status_code, 200, msg='Fetch failed')
    result2JSON = json.loads(result2.get_data(as_text=True))
    expPaginationResult = {'offset': 0, 'pagesize': 20, 'total': 0}
    self.assertJSONStringsEqual(result2JSON["pagination"], expPaginationResult);

  def addExecution(self, jobGUID, jobName):
    result2 = self.testClient.post('/api/jobs/' + jobGUID + '/execution', data=json.dumps({"name": jobName}), content_type='application/json')
    self.assertEqual(result2.status_code, 200)
    return json.loads(result2.get_data(as_text=True))

  def test_submitJobForExecution(self):
    result = self.testClient.post('/api/jobs/', data=json.dumps(data_simpleJobCreateParams), content_type='application/json')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    jobGUID = resultJSON['guid']
    jobCommand = resultJSON['command']
    self.assertEqual(len(jobGUID),36, msg='Invalid job GUID - must be 36 chars')

    resultJSON2 = self.addExecution(jobGUID, 'TestExecutionName')
    exp = dict(data_simpleJobExecutionCreateExpRes)
    resultJSON2['guid'] = exp['guid']
    resultJSON2['dateCreated'] = exp['dateCreated']
    resultJSON2['dateStarted'] = exp['dateStarted']
    resultJSON2['dateCompleted'] = exp['dateCompleted']

    exp['jobCommand'] = jobCommand
    exp['jobGUID'] = jobGUID

    self.assertJSONStringsEqual(resultJSON2, exp);

  def test_getJobExecutions(self):
    #add a load of jobs, then add two jobs we will put executions against
    # call back executions and check we get executions for only one of the two jobs
    self.createJobs(10, data_simpleJobCreateParams)
    jobOneCreateParams = dict(data_simpleJobCreateParams)
    jobOneCreateParams['name'] = 'TestJobOne'
    jobTwoCreateParams = dict(data_simpleJobCreateParams)
    jobTwoCreateParams['name'] = 'TestJobTwo'
    result = self.testClient.post('/api/jobs/', data=json.dumps(jobOneCreateParams), content_type='application/json')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    jobOneGUID = resultJSON['guid']
    result = self.testClient.post('/api/jobs/', data=json.dumps(jobTwoCreateParams), content_type='application/json')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    jobTwoGUID = resultJSON['guid']

    # Add two executions for job one
    execution_guids = {}
    result2 = self.addExecution(jobOneGUID, '001_001')
    execution_guids['001_001'] = result2['guid']
    result2 = self.addExecution(jobOneGUID, '001_002')
    execution_guids['001_002'] = result2['guid']

    # Add two executions for job two
    result2 = self.addExecution(jobTwoGUID, '002_001')
    execution_guids['002_001'] = result2['guid']
    result2 = self.addExecution(jobTwoGUID, '002_002')
    execution_guids['002_002'] = result2['guid']

    #Retreieve executions for job one and make sure we only get two and they match the two we put in
    queryJobExecutionsForJobOneResult = self.testClient.get('/api/jobs/' + jobOneGUID + '/execution')
    self.assertEqual(queryJobExecutionsForJobOneResult.status_code, 200)
    queryJobExecutionsForJobOneResultJSON = json.loads(queryJobExecutionsForJobOneResult.get_data(as_text=True))

    #We should only get two results returned
    self.assertJSONStringsEqual(queryJobExecutionsForJobOneResultJSON["pagination"]["total"], 2, msg='Expected to get 2 executions for job one');
    executionOneSeen = False
    executionTwoSeen = False
    #Check Correct execution GUID's returned
    for cur in range(0,queryJobExecutionsForJobOneResultJSON["pagination"]["total"]):
      self.assertEqual(queryJobExecutionsForJobOneResultJSON["result"][cur]["jobGUID"],jobOneGUID, msg='Execution for job one has not got jobGUID matching one job')
      #exp['name'] = param2[cur]['name']
      #self.assertJSONJobStringsEqual(result2JSON["result"][cur], exp);
      if queryJobExecutionsForJobOneResultJSON["result"][cur]["guid"] == execution_guids['001_001']:
        if executionOneSeen:
          self.assertTrue(False, msg='Returned execution one twice')
        executionOneSeen = True
      if queryJobExecutionsForJobOneResultJSON["result"][cur]["guid"] == execution_guids['001_002']:
        if executionTwoSeen:
          self.assertTrue(False, msg='Returned execution two twice')
        executionTwoSeen = True
      #print(queryJobExecutionsForJobOneResultJSON["result"][cur]["guid"])
    if not executionOneSeen:
      self.assertTrue(False, msg='Execution one not returned')
    if not executionTwoSeen:
      self.assertTrue(False, msg='Execution two not returned')



