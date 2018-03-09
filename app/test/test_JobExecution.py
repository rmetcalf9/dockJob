#tests for appObj
from TestHelperSuperClass import testHelperAPIClient
from JobExecution import JobExecutionClass

class test_JobExecution(testHelperAPIClient):

  def test_Create(self):
    jobObj = {'GUID': 'a', 'command': 'a'}
    a = JobExecutionClass(jobObj)
    self.assertEqual(a.stage, 'Pending')

