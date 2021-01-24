import TestHelperSuperClass
import TestHelperWithAPIOperations
import unittest
import json
from commonJSONStrings import data_simpleJobCreateParams, data_simpleJobCreateExpRes, data_simpleManualJobCreateParams
import jobsDataObj
import jobObj
from appObj import appObj

class helperClass(TestHelperWithAPIOperations.TestHelperWithAPIOperationsClass):
  pass

#@TestHelperSuperClass.wipd
class test_jobsDataAPI_deleteLogic(helperClass):

  def test_deleteJobCausesJobsThatUseItToBecomeRemoved(self):
    mainJobJSON = self.createJob(name="mainJob")
    jobThatCallsMainJObJSON = self.createJob(name="jobThatCallsMainJob", stateChangeSuccessJobGUID=mainJobJSON["guid"])

    checkJobThatCallsMainJobJSON = self.getJob(guid=jobThatCallsMainJObJSON["guid"])
    self.assertEqual(checkJobThatCallsMainJobJSON["StateChangeSuccessJobGUID"], mainJobJSON["guid"])
    self.assertEqual(checkJobThatCallsMainJobJSON["StateChangeSuccessJobNAME"], mainJobJSON["name"])

    self.deleteJob(guid=mainJobJSON["guid"])

    check2JobThatCallsMainJobJSON = self.getJob(guid=jobThatCallsMainJObJSON["guid"])
    self.assertEqual(check2JobThatCallsMainJobJSON["StateChangeSuccessJobGUID"], None)
    self.assertEqual(check2JobThatCallsMainJobJSON["StateChangeSuccessJobNAME"], None)
