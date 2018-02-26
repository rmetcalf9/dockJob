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
  def test_JobCreate(self):
    result = self.testClient.post('/api/jobs/', data=json.dumps(data_simpleJobCreateParams), content_type='application/json')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertTrue(len(resultJSON['guid']) == 36, msg='Invalid GUID - must be 36 chars')
    self.assertTrue(resultJSON['creationDate'] == resultJSON['lastUpdateDate'], msg='Creation date dosen''t match last update')
    tim = from_iso8601(resultJSON['creationDate'])
    self.assertTimeCloseToCurrent(tim)
    resultJSON['guid'] = data_simpleJobCreateExpRes['guid']
    resultJSON['nextScheduledRun'] = data_simpleJobCreateExpRes['nextScheduledRun']
    resultJSON['creationDate'] = data_simpleJobCreateExpRes['creationDate']
    resultJSON['lastUpdateDate'] = data_simpleJobCreateExpRes['lastUpdateDate']
    self.assertJSONStringsEqual(resultJSON, data_simpleJobCreateExpRes);

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
    resultJSON['guid'] = data_simpleJobCreateExpRes['guid']
    resultJSON['nextScheduledRun'] = data_simpleJobCreateExpRes['nextScheduledRun']
    resultJSON['creationDate'] = data_simpleJobCreateExpRes['creationDate']
    resultJSON['lastUpdateDate'] = data_simpleJobCreateExpRes['lastUpdateDate']
    self.assertJSONStringsEqual(resultJSON, data_simpleJobCreateExpRes);

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
    resultJSON['guid'] = data_simpleJobCreateExpRes['guid']
    resultJSON['nextScheduledRun'] = data_simpleJobCreateExpRes['nextScheduledRun']
    resultJSON['creationDate'] = data_simpleJobCreateExpRes['creationDate']
    resultJSON['lastUpdateDate'] = data_simpleJobCreateExpRes['lastUpdateDate']
    self.assertJSONStringsEqual(resultJSON, data_simpleJobCreateExpRes);

  def test_jobCreateAndQueryBackByName(self):
    for cur in range(1, 6):
      param = dict(data_simpleJobCreateParams)
      param['name'] = data_simpleJobCreateParams['name'] + str(cur)
      result = self.testClient.post('/api/jobs/', data=json.dumps(param), content_type='application/json')
      self.assertEqual(result.status_code, 200, msg='job creation failed')
    result2 = self.testClient.get('/api/jobs/')
    self.assertEqual(result.status_code, 200, msg='Fetch failed')
    result2JSON = json.loads(result2.get_data(as_text=True))
    expPaginationResult = {'offset': 0, 'pagesize': 20, 'total': 5}
    self.assertJSONStringsEqual(result2JSON["pagination"], expPaginationResult);
    self.assertEqual(len(result2JSON["result"]),5,msg="Wrong number of returned results")
    exp = data_simpleJobCreateExpRes
    for cur in range(0,5):
      rem = len(result2JSON["result"][cur]['name']) - len(data_simpleJobCreateParams['name'])
      result2JSON["result"][cur]['name'] = result2JSON["result"][cur]['name'][:(-1 * rem)]
      result2JSON["result"][cur]['guid'] = data_simpleJobCreateExpRes['guid']
      result2JSON["result"][cur]['nextScheduledRun'] = data_simpleJobCreateExpRes['nextScheduledRun']
      result2JSON["result"][cur]['creationDate'] = data_simpleJobCreateExpRes['creationDate']
      result2JSON["result"][cur]['lastUpdateDate'] = data_simpleJobCreateExpRes['lastUpdateDate']
      self.assertJSONStringsEqual(result2JSON["result"][cur], exp);

#Delete job by GUID
#Delete job by GUID error not exist
#Delete job by name
#Delete job by name error not exist


#Query back 30 jobs (pagination test)
#Query back 2nd page
#Query back part of page



