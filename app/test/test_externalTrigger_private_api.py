# This tests activateing and deactivataing an API on a job

from TestHelperSuperClass import testHelperAPIClient, env
import json
from commonJSONStrings import data_simpleJobCreateParams, data_simpleJobCreateExpRes, data_simpleManualJobCreateParams
import pytest
from appObj import appObj
import copy

class helper(testHelperAPIClient):
    def setup(self):
        result = self.testClient.post('/api/jobs/', data=json.dumps(data_simpleJobCreateParams), content_type='application/json')
        self.assertResponseCodeEqual(result, 200)
        return {
            "setupJob": json.loads(result.text)
        }

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
        self.assertEqual(apiResultTMP.status_code, 201, msg=msg + " " + apiResultTMP.get_data(as_text=True))
        return json.loads(apiResultTMP.get_data(as_text=True))

    def getJob(self, jobguid, msg="", check_and_parse_response=True):
        apiResultTMP = self.testClient.get('/api/jobs/' +jobguid)
        if not check_and_parse_response:
            return apiResultTMP
        self.assertEqual(apiResultTMP.status_code, 200, msg=msg)
        return json.loads(apiResultTMP)

@pytest.mark.externalTriggerSystemTest
class test_externalTrigger_private_api(helper):

  def test_activateapionjob_invalidtyoe(self):
      setup = self.setup()

      activate_response = self.activateTriggerOnJob(
          jobGuid = setup["setupJob"]["guid"],
          triggerType="googleDriveRawClassXXX",
          triggerOptions={},
          check_and_parse_response=False
      )
      self.assertEqual(activate_response.status_code, 400)
      response_json = json.loads(activate_response.text)
      self.assertEqual(response_json["result"], "Fail")
      self.assertEqual(response_json["message"], "Invalid trigger type")

  def test_activateapionjob_nonexistantjob(self):
      activate_response = self.activateTriggerOnJob(
          jobGuid = "npn esistant job",
          triggerType="googleDriveRawClass",
          triggerOptions={},
          check_and_parse_response=False
      )
      print("DDD", activate_response.text)
      self.assertEqual(activate_response.status_code, 404)
      response_json = json.loads(activate_response.text)
      self.assertEqual(response_json["result"], "Fail")
      self.assertEqual(response_json["message"], "Job not found")

  # def test_activateapionjob(self):
  #     setup = self.setup()
  #
  #     activate_response = self.activateTriggerOnJob(
  #         jobGuid = setup["setupJob"]["guid"],
  #         triggerType="googleDriveRawClass",
  #         triggerOptions={}
  #     )
  #
  #     # expectedTriggerTypeJson = {
  #     #   "active": True,
  #     #   "type": "googleDriveRawClass"
  #     #   "urlpasscode": String set to a guid
  #     #   "nonurlpasscode": String set to a guid
  #     #   "salt" base64 string,
  #     #   "typeprivatevars": JSON defined by type
  #     #   "typepublicvars": JSON defined by type
  #     # }
  #
  #     def checkTriggerTypeIsOk(recieved):
  #         self.assertEqual(recieved["active"], True)
  #         self.assertEqual(recieved["type"], "googleDriveRawClass")
  #         #TODO check keys salt and vars
  #     checkTriggerTypeIsOk(activate_response)
  #
  #     #Get job
  #     get_job_response = self.getJob(jobguid=setup["setupJob"]["guid"])
  #     checkTriggerTypeIsOk(get_job_response)

#TODO Test activateing when trigger is already active
# Keys must have changed