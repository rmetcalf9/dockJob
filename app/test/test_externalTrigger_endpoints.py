# This tests the external trigger endpoints
#  makes sure they fire at the correct URL
#  and make sure protected API's do not fire at that url

from TestHelperSuperClass import testHelperAPIClient, env
import unittest
import json
from commonJSONStrings import data_simpleJobCreateParams, data_simpleJobCreateExpRes, data_simpleManualJobCreateParams
import pytest
from appObj import appObj
import copy
from TestHelperWithAPIOperations import TestHelperWithAPIOperationsClass
from encryption import decryptPassword
import time

normal_api_prefix = "/api"
external_trigger_api_prefix = "triggerapi"

example_changes_recource_message = {
    "headers": {
        "Content-Type": "application/json; utf-8",
        ##"Content-Length": "118", letting requests work this out for me
        "X-Goog-Channel-ID": "8bd90be9-3a58-3122-ab43-9823188a5b43",
        "X-Goog-Channel-Token": "245t1234tt83trrt333",  #This is going to be the encoded job GUID
        "X-Goog-Channel-Expiration": "Tue, 19 Nov 2013 01:13:52 GMT",
        "X-Goog-Resource-ID":  "ret987df98743md8g",
        "X-Goog-Resource-URI": "https://www.googleapis.com/drive/v3/changes",
        "X-Goog-Resource-State":  "changed",
        "X-Goog-Message-Number": "23"

    },
    "data": json.dumps({
      "kind": "drive#changes"
    })
}

class helper(TestHelperWithAPIOperationsClass):
    def get_executions_for_job(self, job_guid):
        reqURL = '/api/jobs/' + job_guid + '/execution'
        queryJobExecutionsResult = self.testClient.get(reqURL)
        self.assertEqual(queryJobExecutionsResult.status_code, 200, msg='Request to ' + reqURL + ' failed')
        resDict = json.loads(queryJobExecutionsResult.text)
        return resDict

@pytest.mark.externalTriggerSystemTest
class test_externalTriggerEndpoints(helper):

  def test_getStaticServerInfoFromRealEndpoint(self):
      result = self.testClient.get(normal_api_prefix + '/serverinfo')
      self.assertEqual(result.status_code, 200)

  def test_getStaticServerInfoFromTriggerEndpoint_returns_not_found(self):
      result = self.testClient.get(external_trigger_api_prefix + '/serverinfo')
      self.assertEqual(result.status_code, 404)

  def test_trigger_endpoints_report_ok(self):
      result = self.testClient.get(external_trigger_api_prefix + '/up')
      self.assertEqual(result.status_code, 200)
      resultDict = json.loads(result.text)
      self.assertEqual(resultDict["result"], "Success")

# 406 means message was received but there are no configured types to process
  def test_trigger_endpoint_with_no_configured_job_returns_406(self):
      sample_post_data = None
      sample_headers = {}
      result = self.testClient.post(
          external_trigger_api_prefix + '/trigger/anything',
          data=example_changes_recource_message["data"],
          headers=example_changes_recource_message["headers"]
      )
      self.assertEqual(result.status_code, 406)

  def test_trigger_endpoint_valid_job_is_but_job_does_not_exist(self):
    sample_valid_encoded_job_guid = appObj.externalTriggerManager.encodeJobGuid("fake_job_guid")
    resource_message = copy.deepcopy(example_changes_recource_message)
    resource_message["headers"]["X-Goog-Channel-Token"] = sample_valid_encoded_job_guid
    result = self.testClient.post(
        external_trigger_api_prefix + '/trigger/anything',
        data=resource_message["data"],
        headers=resource_message["headers"]
    )
    self.assertEqual(result.status_code, 406)

  def test_trigger_endpoint_valid_job_with_no_trigger_active(self):
      jobData = self.createJob()

      encoded_job_guid = appObj.externalTriggerManager.encodeJobGuid(jobData["guid"])
      decoded_job_guid = appObj.externalTriggerManager.decodeJobGuid(encoded_job_guid)
      self.assertEqual(jobData["guid"], decoded_job_guid)

      #Add job ID to message
      resource_message = copy.deepcopy(example_changes_recource_message)
      resource_message["headers"]["X-Goog-Channel-Token"] = encoded_job_guid

      result = self.testClient.post(
          external_trigger_api_prefix + '/trigger/anything',
          data=resource_message["data"],
          headers=resource_message["headers"]
      )
      self.assertEqual(result.status_code, 406)

  def test_trigger_endpoint_valid_job_wrong_passcodes_returns_403(self):
      jobData = self.createJob()

      encoded_job_guid = appObj.externalTriggerManager.encodeJobGuid(jobData["guid"])
      decoded_job_guid = appObj.externalTriggerManager.decodeJobGuid(encoded_job_guid)
      self.assertEqual(jobData["guid"], decoded_job_guid)

      #Add job ID to message
      resource_message = copy.deepcopy(example_changes_recource_message)
      resource_message["headers"]["X-Goog-Channel-Token"] = encoded_job_guid

      result = self.testClient.post(
          external_trigger_api_prefix + '/trigger/anything',
          data=resource_message["data"],
          headers=resource_message["headers"]
      )
      self.assertEqual(result.status_code, 406)

  def test_trigger_endpoint_valid_job_only_url_passcode_right_fails(self):
      jobData = self.createJob()
      activate_response = self.activateTriggerOnJob(
          jobGuid = jobData["guid"],
          triggerType="googleDriveRawClass",
          triggerOptions={}
      )
      encoded_job_guid = appObj.externalTriggerManager.encodeJobGuid(jobData["guid"])

      #Add job ID to message
      resource_message = copy.deepcopy(example_changes_recource_message)
      resource_message["headers"]["X-Goog-Channel-Token"] = encoded_job_guid

      ExternalTrigger = activate_response["ExternalTrigger"]
      rawurlpasscode = ExternalTrigger["urlpasscode"]

      result = self.testClient.post(
          external_trigger_api_prefix + '/trigger/' + rawurlpasscode,
          data=resource_message["data"],
          headers=resource_message["headers"]
      )
      self.assertEqual(result.status_code, 406)

  def test_trigger_endpoint_valid_job_only_nonurlpasscode_right_fails(self):
      jobData = self.createJob()
      activate_response = self.activateTriggerOnJob(
          jobGuid = jobData["guid"],
          triggerType="googleDriveRawClass",
          triggerOptions={}
      )
      encoded_job_guid = appObj.externalTriggerManager.encodeJobGuid(jobData["guid"])

      #Add job ID to message
      resource_message = copy.deepcopy(example_changes_recource_message)
      resource_message["headers"]["X-Goog-Channel-Token"] = encoded_job_guid

      ExternalTrigger = activate_response["ExternalTrigger"]
      resource_message["headers"]["X-Goog-Channel-ID"]=ExternalTrigger["nonurlpasscode"]

      result = self.testClient.post(
          external_trigger_api_prefix + '/trigger/wrongvalue',
          data=resource_message["data"],
          headers=resource_message["headers"]
      )
      self.assertEqual(result.status_code, 406)

  def test_trigger_endpoint_valid_job_right_passcodes_returns_200(self):
      jobData = self.createJob(command="cat -")
      activate_response = self.activateTriggerOnJob(
          jobGuid = jobData["guid"],
          triggerType="googleDriveRawClass",
          triggerOptions={}
      )
      encoded_job_guid = appObj.externalTriggerManager.encodeJobGuid(jobData["guid"])

      #Add job ID to message
      resource_message = copy.deepcopy(example_changes_recource_message)
      resource_message["headers"]["X-Goog-Channel-Token"] = encoded_job_guid

      ExternalTrigger = activate_response["ExternalTrigger"]
      rawurlpasscode = ExternalTrigger["urlpasscode"]
      rawnonurlpasscode = ExternalTrigger["nonurlpasscode"]
      resource_message["headers"]["X-Goog-Channel-ID"]=rawnonurlpasscode

      result = self.testClient.post(
          external_trigger_api_prefix + '/trigger/' + rawurlpasscode,
          data=resource_message["data"],
          headers=resource_message["headers"]
      )
      self.assertEqual(result.status_code, 200)

      #Find executed job and check stdout
      ## first give the app the chance to complete the job
      appObj.jobExecutor.loopIteration(appObj.getCurDateTime())

      executions_for_job = self.get_executions_for_job(
          job_guid = jobData["guid"]
      )
      self.assertEqual(len(executions_for_job["result"]) ,1, msg="Execution not found")
      stdout_dict = json.loads(executions_for_job["result"][0]["resultSTDOUT"])
      self.assertEqual(stdout_dict["headers"]["X-Goog-Channel-Id"], rawnonurlpasscode)
      self.assertEqual(stdout_dict["headers"]["X-Goog-Channel-Token"], encoded_job_guid)
