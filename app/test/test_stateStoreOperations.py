import TestHelperSuperClass
import unittest
import json
from commonJSONStrings import data_simpleJobCreateParams, data_simpleJobCreateExpRes, data_simpleManualJobCreateParams
import jobsDataObj
import jobObj
from appObj import appObj

sampleJob = jobObj.jobClass(
  appObj=appObj,
  name="sampleJob",
  command="ls -la",
  enabled=False,
  repetitionInterval=None,
  pinned=True,
  overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown=123,
  StateChangeSuccessJobGUID=None,
  StateChangeFailJobGUID=None,
  StateChangeUnknownJobGUID=None
)

class helperClass(TestHelperSuperClass.testHelperAPIClient):
  def addJobToStore(self, objectStore, job):
    storeConnection = objectStore._getConnectionContext()
    def someFn(connectionContext):
      #print(self.jobs[jobGUID]._caculatedDict(self.appObj))
      newObjectVersion = connectionContext.saveJSONObject(
        jobsDataObj.objectType,
        job.guid,
        job._caculatedDict(appObj),
        objectVersion = job.objectVersion
      )
      job.objectVersion = newObjectVersion
    storeConnection.executeInsideTransaction(someFn)

  def objectStorePopulationHook(self, objectStore):
    self.addJobToStore(objectStore=objectStore, job=sampleJob)


@TestHelperSuperClass.wipd
class test_stateStoreOperations(helperClass):

  def test_loadSingleJobFromStore(self):
    result2 = self.testClient.get('/api/jobs/' + sampleJob.guid)
    self.assertEqual(result2.status_code, 200, msg='Job that was in the DB on load is not returned in request')
    result2JSON = json.loads(result2.get_data(as_text=True))
    if result2JSON["repetitionInterval"] == "":
      result2JSON["repetitionInterval"] = None
    self.assertJSONJobStringsEqual(result2JSON, sampleJob._caculatedDict(self.testClient));


