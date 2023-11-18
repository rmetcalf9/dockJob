#Test helper functions
# defines a baseclass with extra functions
# https://docs.python.org/3/library/unittest.html
import unittest
import json
from appObj import appObj
from base64 import b64encode

import datetime
import pytz
from baseapp_for_restapi_backend_with_swagger import from_iso8601

monitorCheckTempStateAPIPrefix = '/api/monitorCheckTempState'

env = {
  'APIAPP_MODE': 'DOCKER',
  'APIAPP_VERSION': 'TEST-3.3.3',
  'APIAPP_FRONTEND': '../app',
  'APIAPP_APIURL': 'http://apiurlxxx',
  'APIAPP_TRIGGERAPIURL': 'http://triggerapiurlxxx',
  'APIAPP_FRONTENDURL': 'http://frontenddummytestxxx',
  'APIAPP_APIDOCSURL': 'something',
  'APIAPP_APIACCESSSECURITY': '[{ "type": "basic-auth" }]',
  'APIAPP_USERFORJOBS': 'root',
  'APIAPP_GROUPFORJOBS': 'root',
  'APIAPP_SKIPUSERCHECK': True,
  'APIAPP_MONITORCHECKTEMPSTATECONFIG': '{ "username": "abc", "password": "123" }',
  'DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD': 'dummy_test_password',
  'DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE': './test/dummy_client_secret.json'
}

class testHelperSuperClass(unittest.TestCase):
  def assertJSONJobStringsEqual(self, result,expectedResult):
    #ignores fields that may be different
    result['guid'] = expectedResult['guid']
    result['nextScheduledRun'] = expectedResult['nextScheduledRun']
    result['creationDate'] = expectedResult['creationDate']
    result['lastUpdateDate'] = expectedResult['lastUpdateDate']
    result['objectVersion'] = expectedResult['objectVersion']
    self.assertJSONStringsEqual(result, expectedResult);

  def checkGotRightException(self, context, ExpectedException):
    if (context.exception != None):
      if (context.exception != ExpectedException):
        print("**** Wrong exception raised:")
        print("      expected: " + type(ExpectedException).__name__ + ' - ' + str(ExpectedException));
        print("           got: " + type(context.exception).__name__ + ' - ' + str(context.exception));
        raise context.exception
    self.assertTrue(ExpectedException == context.exception)

  def areJSONStringsEqual(self, str1, str2):
    a = json.dumps(str1, sort_keys=True)
    b = json.dumps(str2, sort_keys=True)
    return (a == b)

  def assertJSONStringsEqual(self, str1, str2, msg=''):
    if (self.areJSONStringsEqual(str1,str2)):
      return
    print("Mismatch JSON")
    a = json.dumps(str1, sort_keys=True)
    b = json.dumps(str2, sort_keys=True)
    print(a)
    print("--")
    print(b)
    self.assertTrue(False, msg=msg)

  def assertTimeCloseToCurrent(self, time, msg='Creation time is more than 3 seconds adrift'):
    if (isinstance(time, str)):
      time = from_iso8601(time)
    curTime = datetime.datetime.now(pytz.timezone("UTC"))
    time_diff = (curTime - time).total_seconds()
    self.assertTrue(time_diff < 3, msg=msg)

  def assertResponseCodeEqual(self, result, expectedResponse, msg=''):
    if result.status_code==expectedResponse:
      return
    print(result.get_data(as_text=True))
    self.assertEqual(result.status_code, expectedResponse, msg)
    
#helper class with setup for an APIClient
class testHelperAPIClient(testHelperSuperClass):
  testClient = None
  standardStartupTime = pytz.timezone('Europe/London').localize(datetime.datetime(2018,1,1,13,46,0,0))

  def objectStorePopulationHook(self, objectStore):
    pass #designed to be overriden

  def setUp(self):
    # curDatetime = datetime.datetime.now(pytz.utc)
    # for testing always pretend the server started at a set datetime
    appObj.init(env, self.standardStartupTime, testingMode = True, objectStoreTestingPopulationHookFn = self.objectStorePopulationHook)
    self.testClient = appObj.flaskAppObject.test_client()
    self.testClient.testing = True 
  def tearDown(self):
    appObj.stopThread()
    self.testClient = None

  def getTotalJobs(self):
    result2 = self.testClient.get('/api/serverinfo/')
    self.assertEqual(result2.status_code, 200)
    resultJSON = json.loads(result2.get_data(as_text=True))
    return resultJSON['Jobs']['TotalJobs']
    
  def assertCorrectTotalJobs(self, num):
    # Ensure total reflected in serverinfo
    self.assertEqual(self.getTotalJobs(), num, msg='Server Info Total Jobs field not correct')

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
      self.assertResponseCodeEqual(result, 200, msg='job creation failed')
      param[cur]['createResult'] = dict(json.loads(result.get_data(as_text=True)))
    self.assertCorrectTotalJobs(num + jobsAtStart)
    return param

  def addExecution(self, jobGUID, jobName):
    result2 = self.testClient.post('/api/jobs/' + jobGUID + '/execution', data=json.dumps({"name": jobName}), content_type='application/json')
    self.assertEqual(result2.status_code, 200)
    return json.loads(result2.get_data(as_text=True))

  #data_simpleJobCreateParams
  def setupJobsAndExecutions(self, jobCreateParams):
    #Set up some job data and two special jobs each with two executions
    # return the guids of the jobs that were setup with executions

    #add a load of jobs, then add two jobs we will put executions against
    # call back executions and check we get executions for only one of the two jobs
    self.createJobs(10, jobCreateParams)
    jobOneCreateParams = dict(jobCreateParams)
    jobOneCreateParams['name'] = 'TestJobOne'
    jobTwoCreateParams = dict(jobCreateParams)
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

    #Retrieve job executions for job one. Do this twice, once by GUID and again by name
    keysToUse = [ jobOneGUID, jobOneCreateParams['name']]
    for curKey in keysToUse:
      #Retreieve executions for job one and make sure we only get two and they match the two we put in
      queryJobExecutionsForJobOneResult = self.testClient.get('/api/jobs/' + curKey + '/execution')
      self.assertEqual(queryJobExecutionsForJobOneResult.status_code, 200)
      queryJobExecutionsForJobOneResultJSON = json.loads(queryJobExecutionsForJobOneResult.get_data(as_text=True))

      #We should only get two results returned
      self.assertJSONStringsEqual(queryJobExecutionsForJobOneResultJSON["pagination"]["total"], 2, msg='Expected to get 2 executions for job one (Querying by key=' + curKey + ')');
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

    return execution_guids

  # acceptedResultList can be none then never assert
  def assertAPIResult(self, methodFN, url, session, data, headers):
    if session != None:
      headers[constants.jwtHeaderName] = SessionMock.from_Session(session).getJWTToken()
    if methodFN.__name__ == 'get':
      if data != None:
        raise Exception("Trying to send post data to a get request")
    result = methodFN(
      url,
      headers=headers,
      data=json.dumps(data),
      content_type='application/json'
    )
    return result

  def assertMonitorCheckTempStateAPIResult(self, methodFN, url, session, data, credential):
    headers = {}
    if credential != None:
      userAndPassBin = (credential["user"] + ":" + credential["password"]).encode()
      userAndPass = b64encode(userAndPassBin).decode("ascii")
      headers["Authorization"] = 'Basic %s' % userAndPass
    return self.assertAPIResult(methodFN, monitorCheckTempStateAPIPrefix + url, session, data, headers)
