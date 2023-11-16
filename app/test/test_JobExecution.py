#tests for appObj
from TestHelperSuperClass import testHelperAPIClient
from jobsDataAPI import jobClass
from JobExecution import JobExecutionClass
from appObj import appObj
import time
from baseapp_for_restapi_backend_with_swagger import from_iso8601
import threading

class test_JobExecution(testHelperAPIClient):
  JobExecutionLock = threading.Lock()

  def _getJobExecutionObj(self, jobObj):
    return JobExecutionClass(
      jobObj=jobObj,
      executionName='TestExecutionName',
      manual=False,
      curDatetime=appObj.getCurDateTime(),
      triggerJobObj=None,
      triggerExecutionObj=None
    )

  def createJobObj(self, command='echo "This is a test"'):
    return jobClass(
      appObj, 'TestJob123', command, False, '', False, None, None, None, None, None, None, None,
      guid= None,
      verifyDependentJobGuids=True,
      loadingObjectVersion=None,
      PrivateExternalTrigger = {"triggerActive": False}
    )

  def aquireJobExecutionLock(self):
    if not self.JobExecutionLock.acquire(blocking=True, timeout=0.5): #timeout value is in seconds
      raise Exception("Timedout waiting for lock")
      
  def releaseJobExecutionLock(self):
    self.JobExecutionLock.release()

  def registerRunDetails(self, jobGUID, newLastRunDate, newLastRunReturnCode, triggerExecutionObj):
    pass


  def test_Create(self):
    jobObj = self.createJobObj()
    a = self._getJobExecutionObj(jobObj)
    tim = from_iso8601(a.dateCreated)
    self.assertTimeCloseToCurrent(tim)
    self.assertEqual(a.stage, 'Pending')
    self.assertEqual(a.jobGUID, jobObj.guid)
    self.assertEqual(a.jobCommand, jobObj.command)

  def test_run(self):
    jobObj = self.createJobObj()
    a = self._getJobExecutionObj(jobObj)
    a.execute(appObj.jobExecutor, self.aquireJobExecutionLock, self.releaseJobExecutionLock, self.registerRunDetails, appObj)
    self.assertEqual(a.stage, 'Completed')
    self.assertEqual(a.resultReturnCode, 0)
    self.assertEqual(a.resultSTDOUT, 'This is a test')
    self.assertTimeCloseToCurrent(a.dateCreated)
    self.assertTimeCloseToCurrent(a.dateStarted)
    self.assertTimeCloseToCurrent(a.dateCompleted)

  #Time consuming tests commented out
  #def test_timeout(self):
  #  jobObj = jobClass('TestJob123', 'sleep 5', True, '')
  #  a = JobExecutionClass(jobObj)
  #  appObj.jobExecutor.timeout = 1
  #  start_time = time.time()
  #  a.execute(appObj.jobExecutor, self.aquireJobExecutionLock, self.releaseJobExecutionLock, self.registerRunDetails, appObj)
  #  elapsed_time = time.time() - start_time
  #  self.assertLess(elapsed_time, 2)
  #  self.assertEqual(a.stage, 'Timeout')
  #  self.assertEqual(a.resultReturnCode, -1)

  #I don't hcreateJobObjave this test working yet
  #def test_bigoutput(self):
  #  jobObj = jobClass('TestJob123', 'find /', True, '')
  #  a = JobExecutionClass(jobObj)
  #  appObj.jobExecutor.timeout = 1 #Increase
  #  a.execute(appObj.jobExecutor, self.aquireJobExecutionLock, self.releaseJobExecutionLock, self.registerRunDetails, appObj)
  #  self.assertEqual(a.stage, 'Completed')
  #  self.assertEqual(a.resultReturnCode, 0)

  def test_dictOut(self):
    jobObj = self.createJobObj()
    expPending = {
      'guid': 'OVERRIDE',
      'stage': 'Pending',
      'jobGUID': jobObj.guid,
      'jobName': jobObj.name,
      'jobCommand': jobObj.command,
      'dateCreated': 'OVERRIDE',
      'dateStarted': None,
      'dateCompleted': None,
      'resultReturnCode': None,
      'resultSTDOUT': None,
      'executionName': 'TestExecutionName',
      'manual': False
    }
    expCompleted = dict(expPending)
    expCompleted['resultSTDOUT'] = 'This is a test'
    expCompleted['stage'] = 'Completed'
    expCompleted['dateStarted'] = 'OVERRIDE'
    expCompleted['dateCompleted'] = 'OVERRIDE'
    expCompleted['resultReturnCode'] = 0
    a = self._getJobExecutionObj(jobObj)
    resDict = dict(a._caculatedDict())
    tim = from_iso8601(a.dateCreated)
    resDict['dateCreated'] = 'OVERRIDE'
    resDict['guid'] = 'OVERRIDE'
    self.assertJSONStringsEqual(resDict, expPending)
    a.execute(appObj.jobExecutor, self.aquireJobExecutionLock, self.releaseJobExecutionLock, self.registerRunDetails, appObj)
    self.assertEqual(a.stage, 'Completed')
    resDict = dict(a._caculatedDict())
    resDict['dateCreated'] = 'OVERRIDE'
    resDict['dateStarted'] = 'OVERRIDE'
    resDict['dateCompleted'] = 'OVERRIDE'
    resDict['guid'] = 'OVERRIDE'
    tim = from_iso8601(a.dateStarted)
    self.assertTimeCloseToCurrent(tim)
    tim = from_iso8601(a.dateCompleted)
    self.assertTimeCloseToCurrent(tim)
    self.assertJSONStringsEqual(resDict, expCompleted)

  # Test added in issue https://github.com/rmetcalf9/dockJob/issues/52 when I discovered
  def test_butEncounteredWithWgetFromGoogleFixed(self):
    jobObj = self.createJobObj(command='cat test/wget_google_example.dat | iconv -f ISO-8859-1 -t UTF-8')
    a = self._getJobExecutionObj(jobObj)
    a.execute(appObj.jobExecutor, self.aquireJobExecutionLock, self.releaseJobExecutionLock, self.registerRunDetails, appObj)
    self.assertEqual(a.stage, 'Completed')
    self.assertEqual(a.resultReturnCode, 0)
    self.assertTimeCloseToCurrent(a.dateCreated)
    self.assertTimeCloseToCurrent(a.dateStarted)
    self.assertTimeCloseToCurrent(a.dateCompleted)

  def test_butEncounteredWithWgetFromGoogle(self):
    jobObj = self.createJobObj(command='cat test/wget_google_example.dat')
    a = self._getJobExecutionObj(jobObj)
    a.execute(appObj.jobExecutor, self.aquireJobExecutionLock, self.releaseJobExecutionLock, self.registerRunDetails, appObj)
    self.assertEqual(a.stage, 'Completed')
    self.assertEqual(a.resultReturnCode, 0)
    self.assertTimeCloseToCurrent(a.dateCreated)
    self.assertTimeCloseToCurrent(a.dateStarted)
    self.assertTimeCloseToCurrent(a.dateCompleted)
    self.assertEqual(a.resultSTDOUT, 'ERROR - failed to decode output probally because it wasn\'t in utf-8 format')


