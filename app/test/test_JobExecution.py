#tests for appObj
from TestHelperSuperClass import testHelperAPIClient
from jobsDataAPI import jobClass
from JobExecution import JobExecutionClass
from appObj import appObj
import time

class test_JobExecution(testHelperAPIClient):

  def test_Create(self):
    jobObj = jobClass('TestJob123', 'echo "This is a test"', True, '')
    a = JobExecutionClass(jobObj)
    self.assertEqual(a.stage, 'Pending')
    self.assertEqual(a.jobGUID, jobObj.guid)
    self.assertEqual(a.jobCommand, jobObj.command)

  def test_run(self):
    jobObj = jobClass('TestJob123', 'echo "This is a test"', True, '')
    a = JobExecutionClass(jobObj)
    a.execute(appObj.jobExecutor)
    self.assertEqual(a.stage, 'Completed')
    self.assertEqual(a.resultReturnCode, 0)
    self.assertEqual(a.resultSTDOUT.decode().strip(), 'This is a test')

  #def test_timeout(self):
  #  jobObj = jobClass('TestJob123', 'sleep 5', True, '')
  #  a = JobExecutionClass(jobObj)
  #  appObj.jobExecutor.timeout = 1
  #  start_time = time.time()
  #  a.execute(appObj.jobExecutor)
  #  elapsed_time = time.time() - start_time
  #  self.assertLess(elapsed_time, 2)
  #  self.assertEqual(a.stage, 'Timeout')
  #  self.assertEqual(a.resultReturnCode, -1)

  #I don't have this test working yet
  #def test_bigoutput(self):
  #  jobObj = jobClass('TestJob123', 'find /', True, '')
  #  a = JobExecutionClass(jobObj)
  #  appObj.jobExecutor.timeout = 1 #Increase
  #  a.execute(appObj.jobExecutor)
  #  self.assertEqual(a.stage, 'Completed')
  #  self.assertEqual(a.resultReturnCode, 0)
