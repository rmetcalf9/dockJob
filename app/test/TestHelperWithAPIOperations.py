import TestHelperSuperClass
import json
from commonJSONStrings import data_simpleManualJobCreateParams
import copy

class TestHelperWithAPIOperationsClass(TestHelperSuperClass.testHelperAPIClient):

  def createJob(
    self,
    name="TestJob",
    repetitionInterval="",
    command="ls -la",
    enabled=False,
    checkAndParseResponse=True,
    stateChangeSuccessJobGUID=None,
    msg=""
  ):
    createDict = {
      "name": name,
      "repetitionInterval": repetitionInterval,
      "command": command,
      "enabled": enabled
    }
    if stateChangeSuccessJobGUID is not None:
      createDict["StateChangeSuccessJobGUID"] = stateChangeSuccessJobGUID

    result = self.testClient.post('/api/jobs/', data=json.dumps(createDict), content_type='application/json')

    if not checkAndParseResponse:
      return result
    self.assertEqual(result.status_code, 200, str(msg) + " - " + result.get_data(as_text=True))
    return json.loads(result.get_data(as_text=True))

  def getJob(
    self,
    guid,
    checkAndParseResponse=True,
    msg=""
  ):
    result = self.testClient.get('/api/jobs/' + guid, data=None, content_type='application/json')

    if not checkAndParseResponse:
      return result
    self.assertEqual(result.status_code, 200, str(msg) + " - " + result.get_data(as_text=True))
    return json.loads(result.get_data(as_text=True))

  def deleteJob(
    self,
    guid,
    checkAndParseResponse=True,
    msg=""
  ):
    result = self.testClient.delete('/api/jobs/' + guid, data=None, content_type='application/json')

    if not checkAndParseResponse:
      return result
    self.assertEqual(result.status_code, 200, str(msg) + " - " + result.get_data(as_text=True))
    return json.loads(result.get_data(as_text=True))

  def activateTriggerOnJob(self, jobGuid, triggerType, triggerOptions, msg="", check_and_parse_response=True):
    post_data={
        "triggerType": triggerType,
        "triggerOptions": triggerOptions
    }
    apiResultTMP = self.testClient.post(
        '/api/jobs/' + jobGuid + "/activateTrigger", data=json.dumps(post_data), content_type='application/json'
    )

    if not check_and_parse_response:
        return apiResultTMP
    if apiResultTMP.status_code == 201:
      return json.loads(apiResultTMP.get_data(as_text=True))
    print("ERROR activateTriggerOnJob failed")
    print("Status:", apiResultTMP.status_code)
    print("Body:", apiResultTMP.text)
    self.assertTrue(False)