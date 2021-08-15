from TestHelperSuperClass import testHelperAPIClient

import TestHelperSuperClass
import json
import uuid

from baseapp_for_restapi_backend_with_swagger import from_iso8601
from appObj import appObj
import datetime
import pytz
import time
import copy
from jobsDataObj import jobsDataClass
from dateutil.relativedelta import relativedelta
from commonJSONStrings import data_simpleJobCreateParams, data_simpleManualJobCreateParams, data_simpleJobCreateExpRes, data_simpleJobExecutionCreateExpRes, data_simpleManualJobCreateParamsWithAllOptionalFields, data_simpleManualJobCreateParamsWithAllOptionalFieldsExpRes

validCredentails = {
  "user": "abc",
  "password": "123"
}
wrongPasswordCredentails = {
  "user": "abc",
  "password": "123ThisIsWrong"
}

class helper(testHelperAPIClient):
  apiPath = ""

  def storeNumber(self, uuidStr, number, credential, msg="", checkAndParseResponse=True):
    postData = {
      "value": number
    }
    result = self.assertMonitorCheckTempStateAPIResult(
      methodFN=self.testClient.post,
      url=self.apiPath + "/" + uuidStr,
      session=None,
      data=postData,
      credential = credential
    )
    if not checkAndParseResponse:
      return result
    self.assertEqual(result.status_code, 200, str(msg) + " - " + result.get_data(as_text=True))
    return json.loads(result.get_data(as_text=True))

  def getNumber(self, uuidStr, credential, msg="", checkAndParseResponse=True):
    result = self.assertMonitorCheckTempStateAPIResult(
      methodFN=self.testClient.get,
      url=self.apiPath + "/" + uuidStr,
      session=None,
      data=None,
      credential = credential
    )
    if not checkAndParseResponse:
      return result
    self.assertEqual(result.status_code, 200, str(msg) + " - " + result.get_data(as_text=True))
    return json.loads(result.get_data(as_text=True))


@TestHelperSuperClass.wipd
class test_jobsData(helper):

  def test_nodatasent_errors(self):
    uuidStr = str(uuid.uuid4())
    result = self.assertMonitorCheckTempStateAPIResult(
      methodFN=self.testClient.post,
      url=self.apiPath + "/" + uuidStr,
      session=None,
      data=None,
      credential = validCredentails
    )
    self.assertEqual(result.status_code, 400, "Error - " + result.get_data(as_text=True))
    self.assertEqual(result.get_data(as_text=True).strip(), "{\"message\": \"value should not be empty\"}".strip())

  def test_post_noCredentialGet_unauthorized(self):
    uuidStr = str(uuid.uuid4())
    response = self.storeNumber(
      uuidStr = uuidStr,
      number = "345",
      credential = None,
      msg= "",
      checkAndParseResponse = False
    )
    self.assertEqual(response.status_code, 401)

  def test_get_noCredentialGet_unauthorized(self):
    uuidStr = str(uuid.uuid4())
    response = self.getNumber(
      uuidStr = uuidStr,
      credential = None,
      msg= "",
      checkAndParseResponse = False
    )
    self.assertEqual(response.status_code, 401)

  def test_post_wrongPassword_forbidden(self):
    uuidStr = str(uuid.uuid4())
    response = self.storeNumber(
      uuidStr = uuidStr,
      number = "345",
      credential = wrongPasswordCredentails,
      msg= "",
      checkAndParseResponse = False
    )
    self.assertEqual(response.status_code, 403)

  def test_get_wrongPassword_forbidden(self):
    uuidStr = str(uuid.uuid4())
    response = self.getNumber(
      uuidStr = uuidStr,
      credential = wrongPasswordCredentails,
      msg= "",
      checkAndParseResponse = False
    )
    self.assertEqual(response.status_code, 403)

  def test_post_invaliduuid_failed(self):
    uuidStr = "INVALID"
    response = self.storeNumber(
      uuidStr = uuidStr,
      number = "345",
      credential = validCredentails,
      msg= "",
      checkAndParseResponse = False
    )
    self.assertEqual(response.status_code, 400)

  def test_get_invaliduuid_failed(self):
    uuidStr = "INVALID"
    response = self.getNumber(
      uuidStr = uuidStr,
      credential = validCredentails,
      msg= "",
      checkAndParseResponse = False
    )
    self.assertEqual(response.status_code, 400)

  def test_post_invalidnumber_failed(self):
    uuidStr = str(uuid.uuid4())
    response = self.storeNumber(
      uuidStr = uuidStr,
      number = "abc345",
      credential = validCredentails,
      msg= "",
      checkAndParseResponse = False
    )
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.get_data(as_text=True).strip(), "{\"message\": \"value must be a number\"}".strip())


# TODO Test number not found
# TODO Test only 10 stored, last one drops off