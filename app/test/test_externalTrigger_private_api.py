# This tests activateing and deactivataing an API on a job

from TestHelperSuperClass import testHelperAPIClient, env
import json
from commonJSONStrings import data_simpleJobCreateParams, data_simpleJobCreateExpRes, data_simpleManualJobCreateParams
import pytest
from appObj import appObj
import copy
from TestHelperWithAPIOperations import TestHelperWithAPIOperationsClass

class helper(TestHelperWithAPIOperationsClass):
    def setup(self):
        result = self.testClient.post('/api/jobs/', data=json.dumps(data_simpleJobCreateParams), content_type='application/json')
        self.assertResponseCodeEqual(result, 200)
        return {
            "setupJob": json.loads(result.text)
        }
    def deactivateTriggerOnJob(self, jobGuid, msg="", check_and_parse_response=True):
        post_data={}
        apiResultTMP = self.testClient.post(
            '/api/jobs/' + jobGuid + "/deactivateTrigger", data=json.dumps(post_data), content_type='application/json'
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
        return json.loads(apiResultTMP.text)

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
      self.assertEqual(activate_response.status_code, 404)
      response_json = json.loads(activate_response.text)
      self.assertEqual(response_json["result"], "Fail")
      self.assertEqual(response_json["message"], "Job not found")

  def test_activateapionjob(self):
      setup = self.setup()

      activate_response = self.activateTriggerOnJob(
          jobGuid = setup["setupJob"]["guid"],
          triggerType="googleDriveRawClass",
          triggerOptions={}
      )
      def checkTriggerTypeIsOk(recieved):
          self.assertEqual(recieved["triggerActive"], True)
          self.assertEqual(recieved["type"], "googleDriveRawClass")
          self.assertTrue(len(recieved["type"])> 0)
          def valid_passcode(passcode):
              #a = passcode.split(":")
              #self.assertEqual(len(a),2)
              #self.assertTrue(len(a[0])>0)
              #self.assertTrue(len(a[1])>0)
              self.assertTrue(len(passcode)>0)

          valid_passcode(recieved["urlpasscode"])
          valid_passcode(recieved["nonurlpasscode"])
          #self.assertEqual(recieved["typepublicvars"], {}) won't be there at all due to skip_none
      checkTriggerTypeIsOk(activate_response["ExternalTrigger"])

      #Get job
      get_job_response = self.getJob(jobguid=setup["setupJob"]["guid"])
      checkTriggerTypeIsOk(get_job_response["ExternalTrigger"])

  def test_deactivateapionjob_that_was_not_active(self):
      setup = self.setup()

      deactivate_response = self.deactivateTriggerOnJob(
          jobGuid=setup["setupJob"]["guid"],
          check_and_parse_response=False
      )
      self.assertEqual(deactivate_response.status_code, 400)
      response_json = json.loads(deactivate_response.text)
      self.assertEqual(response_json["result"], "Warning")
      self.assertEqual(response_json["message"], "Trigger was not active")

  def test_deactivateapionjob(self):
      setup = self.setup()

      activate_response = self.activateTriggerOnJob(
          jobGuid = setup["setupJob"]["guid"],
          triggerType="googleDriveRawClass",
          triggerOptions={}
      )
      deactivate_response = self.deactivateTriggerOnJob(
          jobGuid=setup["setupJob"]["guid"]
      )
      self.assertEqual(deactivate_response["ExternalTrigger"], {"triggerActive": False})
      get_job_response = self.getJob(jobguid=setup["setupJob"]["guid"])
      self.assertEqual(get_job_response["ExternalTrigger"], {"triggerActive": False})

  def test_activate_when_already_active(self):
      setup = self.setup()

      #The test bycypt uses a constant salt for speed. This puts that back for this test
      import bcrypt
      oldbcrypt = appObj.bcrypt
      appObj.bcrypt = bcrypt

      activate_response = self.activateTriggerOnJob(
          jobGuid = setup["setupJob"]["guid"],
          triggerType="googleDriveRawClass",
          triggerOptions={}
      )
      activate_response2 = self.activateTriggerOnJob(
          jobGuid = setup["setupJob"]["guid"],
          triggerType="googleDriveRawClass",
          triggerOptions={}
      )
      # Not 'salt' will not change because the same salt is returned every time by my test salt function
      for keys_that_should_change in ['urlpasscode', 'nonurlpasscode']:
        self.assertNotEqual(
            activate_response["ExternalTrigger"][keys_that_should_change],
            activate_response2["ExternalTrigger"][keys_that_should_change],
            msg="key didn't change " + keys_that_should_change
        )

      appObj.bcrypt = oldbcrypt
