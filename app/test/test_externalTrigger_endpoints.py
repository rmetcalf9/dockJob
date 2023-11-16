# This tests the external trigger endpoints
#  makes sure they fire at the correct URL
#  and make sure protected API's do not fire at that url

from TestHelperSuperClass import testHelperAPIClient, env
import unittest
import json
from commonJSONStrings import data_simpleJobCreateParams, data_simpleJobCreateExpRes, data_simpleManualJobCreateParams
import pytest

normal_api_prefix = "/api"
external_trigger_api_prefix = "triggerapi"

@pytest.mark.externalTriggerSystemTest
class test_externalTriggerEndpoints(testHelperAPIClient):

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

