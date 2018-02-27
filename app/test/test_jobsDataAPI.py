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
class test_jobsData(testHelperAPIClient):
  def assertJSONJobStringsEqual(self, result,expectedResult):
    #ignores fields that may be different
    result['guid'] = expectedResult['guid']
    result['nextScheduledRun'] = expectedResult['nextScheduledRun']
    result['creationDate'] = expectedResult['creationDate']
    result['lastUpdateDate'] = expectedResult['lastUpdateDate']
    self.assertJSONStringsEqual(result, expectedResult);

  def test_JobCreate(self):
    result = self.testClient.post('/api/jobs/', data=json.dumps(data_simpleJobCreateParams), content_type='application/json')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertTrue(len(resultJSON['guid']) == 36, msg='Invalid GUID - must be 36 chars')
    self.assertTrue(resultJSON['creationDate'] == resultJSON['lastUpdateDate'], msg='Creation date dosen''t match last update')
    tim = from_iso8601(resultJSON['creationDate'])
    self.assertTimeCloseToCurrent(tim)
    self.assertJSONJobStringsEqual(resultJSON, data_simpleJobCreateExpRes);

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
    param = {}
    for cur in range(0, num):
      param[cur] = dict(basis)
      param[cur]['name'] = basis['name'] + str(cur+1).zfill(3)
      result = self.testClient.post('/api/jobs/', data=json.dumps(param[cur]), content_type='application/json')
      self.assertEqual(result.status_code, 200, msg='job creation failed')
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

  def test_jobDeleteByName(self):
    result = self.testClient.post('/api/jobs/', data=json.dumps(data_simpleJobCreateParams), content_type='application/json')
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertEqual(result.status_code, 200, msg='First job creation should have worked')
    result2 = self.testClient.delete('/api/jobs/' + resultJSON['name'])
    self.assertEqual(result2.status_code, 200, msg='Didn''t delete record')
    result2JSON = json.loads(result2.get_data(as_text=True))
    self.assertJSONJobStringsEqual(result2JSON, data_simpleJobCreateExpRes);
    result3 = self.testClient.get('/api/jobs/' + resultJSON['name'])
    self.assertEqual(result3.status_code, 400, msg='Managed to retrieve deleted job by name')
    result4 = self.testClient.get('/api/jobs/' + resultJSON['guid'])
    self.assertEqual(result4.status_code, 400, msg='Managed to retrieve deleted job by guid')

  def test_jobDeleteByGUIDNotExist(self):
    result2 = self.testClient.delete('/api/jobs/' + 'BAD-GUID-OR-NAME')
    self.assertEqual(result2.status_code, 400, msg='Deleted a record')

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
    result2 = self.testClient.get('/api/jobs/?filter=Prr')
    self.assertEqual(result2.status_code, 200, msg='Fetch failed')
    result2JSON = json.loads(result2.get_data(as_text=True))
    expPaginationResult = {'offset': 0, 'pagesize': 20, 'total': numShown}
    self.assertJSONStringsEqual(result2JSON["pagination"], expPaginationResult);
    for cur in range(0,numShown):
      exp['name'] = param2[cur]['name']
      self.assertJSONJobStringsEqual(result2JSON["result"][cur], exp);


