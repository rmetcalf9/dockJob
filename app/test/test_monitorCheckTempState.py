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
    self.assertEqual(result.status_code, 201, str(msg) + " - " + result.get_data(as_text=True))
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


  def test_post_number_canberetrieved(self):
    appObj.resetData()
    numberToStore="1234"
    uuidStr = str(uuid.uuid4())
    response = self.storeNumber(
      uuidStr = uuidStr,
      number = numberToStore,
      credential = validCredentails,
      msg= "",
      checkAndParseResponse = True
    )
    self.assertEqual(response["value"], numberToStore)

    responseFromGet = self.getNumber(
      uuidStr = uuidStr,
      credential = validCredentails,
      msg= "",
      checkAndParseResponse = True
    )
    self.assertEqual(responseFromGet["value"], numberToStore)

  def test_get_numbernotthere_notfound(self):
    appObj.resetData()
    uuidStr = str(uuid.uuid4())
    responseFromGet = self.getNumber(
      uuidStr = uuidStr,
      credential = validCredentails,
      msg= "",
      checkAndParseResponse = False
    )
    self.assertEqual(responseFromGet.status_code, 404)
    self.assertEqual(responseFromGet.get_data(as_text=True).strip(), "{\"value\": null, \"message\": \"No number with that uuid present.\"}".strip())

  def test_post_elevennumbers_firstonenotfound(self):
    appObj.resetData()

    numbersToStore = []
    for a in range(100,110):
      uuidStr2 = str(uuid.uuid4())
      numbersToStore.append((a, uuidStr2))

    # Store first two numbers before the main number
    for b in [numbersToStore[0], numbersToStore[1]]:
      responseStore = self.storeNumber(
        uuidStr=b[1],
        number=b[0],
        credential=validCredentails,
        msg="",
        checkAndParseResponse=True
      )
      self.assertEqual(responseStore["value"], str(b[0]))


    numberToStore="1234"
    uuidStr = str(uuid.uuid4())
    responseStoreFirstNumber = self.storeNumber(
      uuidStr = uuidStr,
      number = numberToStore,
      credential = validCredentails,
      msg= "",
      checkAndParseResponse = True
    )
    self.assertEqual(responseStoreFirstNumber["value"], numberToStore)

    #make sure it is there at least once
    responseFromGet = self.getNumber(
      uuidStr = uuidStr,
      credential = validCredentails,
      msg= "",
      checkAndParseResponse = True
    )
    self.assertEqual(responseFromGet["value"], numberToStore)

    for b in numbersToStore:
      responseStore = self.storeNumber(
        uuidStr=b[1],
        number=b[0],
        credential=validCredentails,
        msg="",
        checkAndParseResponse=True
      )
      self.assertEqual(responseStore["value"], str(b[0]))

    # verify the last 10 we stored
    for b in numbersToStore:
      responseFromGet = self.getNumber(
        uuidStr=b[1],
        credential=validCredentails,
        msg="",
        checkAndParseResponse=True
      )
      self.assertEqual(responseFromGet["value"], str(b[0]))

    responseFromGet = self.getNumber(
      uuidStr = uuidStr,
      credential = validCredentails,
      msg= "",
      checkAndParseResponse = False
    )
    self.assertEqual(responseFromGet.status_code, 404)
    self.assertEqual(responseFromGet.get_data(as_text=True).strip(), "{\"value\": null, \"message\": \"No number with that uuid present.\"}".strip())
