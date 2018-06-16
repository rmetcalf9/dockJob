from TestHelperSuperClass import testHelperAPIClient

import json
from baseapp_for_restapi_backend_with_swagger import from_iso8601
from appObj import appObj
import datetime
import pytz
import time
from dateutil.relativedelta import relativedelta
from commonJSONStrings import data_simpleJobCreateParams, data_simpleManualJobCreateParams, data_simpleJobCreateExpRes, data_simpleJobExecutionCreateExpRes, data_simpleManualJobCreateParamsWithAllOptionalFields, data_simpleManualJobCreateParamsWithAllOptionalFieldsExpRes


class test_jobsData(testHelperAPIClient):
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
    expPaginationResult = {'offset': 0, 'pagesize': 100, 'total': numShown}
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
    expPaginationResult = {'offset': 0, 'pagesize': 100, 'total': numShown}
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
    expPaginationResult = {'offset': 0, 'pagesize': 100, 'total': numShown}
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
    expPaginationResult = {'offset': 0, 'pagesize': 100, 'total': 0}
    self.assertJSONStringsEqual(result2JSON["pagination"], expPaginationResult);

  def test_JobFilterForPinnedJobs(self):
    #Create 2 jobs pinned and 2 that are not pinned
    p1 = dict(data_simpleJobCreateParams)
    p1['name'] = 'PinnnedJob'
    p1['pinned'] = True
    p2 = dict(data_simpleJobCreateParams)
    p2['name'] = 'UnpinnedJob'
    p2['pinned'] = False

    param1 = self.createJobs(2, p1)
    param2 = self.createJobs(2, p2)

    pinned1GUID = param1[0]['createResult']['guid']
    pinned2GUID = param1[1]['createResult']['guid']
    unpinned1GUID = param2[0]['createResult']['guid']
    unpinned2GUID = param2[1]['createResult']['guid']

    result2 = self.testClient.get('/api/jobs/?query=pinned=True')
    self.assertEqual(result2.status_code, 200, msg='Fetch failed')
    result2JSON = json.loads(result2.get_data(as_text=True))
    expPaginationResult = {'offset': 0, 'pagesize': 100, 'total': 2}
    self.assertJSONStringsEqual(result2JSON["pagination"], expPaginationResult);


