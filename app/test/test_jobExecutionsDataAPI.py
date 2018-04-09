from TestHelperSuperClass import testHelperAPIClient
import json
from baseapp_for_restapi_backend_with_swagger import from_iso8601

data_simpleJobCreateParams = {
  "name": "TestJob",
  "repetitionInterval": "HOURLY:03",
  "command": "ls",
  "enabled": True
}


class test_jobExecutionsData(testHelperAPIClient):

  def test_GetExecution(self):
    execution_guids = self.setupJobsAndExecutions(data_simpleJobCreateParams)
    queryJobExecutionsResult = self.testClient.get('/api/executions/')
    self.assertEqual(queryJobExecutionsResult.status_code, 200)
    queryJobExecutionsResultJSON = json.loads(queryJobExecutionsResult.get_data(as_text=True))
    self.assertJSONStringsEqual(queryJobExecutionsResultJSON["pagination"]["total"], 4, msg='Expected to get 4 executions (Querying them all)');

    seen = {}
    for cur in execution_guids:
      seen[cur] = False
    for cur in range(0,queryJobExecutionsResultJSON["pagination"]["total"]):
      curExec = queryJobExecutionsResultJSON["result"][cur]
      seen[curExec['executionName']] = True
    for cur in execution_guids:
      if seen[cur] == False:
        self.assertTrue(False, msg='Execution missing from resultset - ' + cur)

  def test_GetSingleExecution(self):
    execution_guids = self.setupJobsAndExecutions(data_simpleJobCreateParams)
    reqURL = '/api/executions/' + execution_guids['001_001']
    queryJobExecutionsResult = self.testClient.get(reqURL)
    self.assertEqual(queryJobExecutionsResult.status_code, 200, msg='Request to ' + reqURL + ' failed')

  def test_GetInvalidSingleExecution(self):
    reqURL = '/api/executions/aaa123'
    queryJobExecutionsResult = self.testClient.get(reqURL)
    queryJobExecutionsResultJSON = json.loads(queryJobExecutionsResult.get_data(as_text=True))
    self.assertEqual(queryJobExecutionsResult.status_code, 400, msg='Request to ' + reqURL + ' did not fail with error 400')



