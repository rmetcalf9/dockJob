from TestHelperSuperClass import testHelperAPIClient
from JobExecutor import JobExecutorClass
from JobExecution import SimpleJobExecutionClass
import os
from appObj import appObj
import uuid


class test_appObjClass(testHelperAPIClient):

  def test_ExecutorConstructor(self):
    pass

  def test_ExecuteAsThisUser(self):
    thisUID = os.getuid()
    cmdToExecute = 'id -u'
    expResSTDOUT = str(thisUID) + '\n'
    res = appObj.jobExecutor.executeCommand(SimpleJobExecutionClass(cmdToExecute))
    self.assertEqual(res.stdout.decode(), expResSTDOUT)

  def test_ErrorSTDErrOutput(self):
    thisUID = os.getuid()
    cmdToExecute = 'sadgfdhgf'
    expResSTDOUT = '/bin/sh: 1: sadgfdhgf: not found\n'
    res = appObj.jobExecutor.executeCommand(SimpleJobExecutionClass(cmdToExecute))
    self.assertEqual(res.stdout.decode(), expResSTDOUT)

  def test_MultipleCommandsWithMixedOutput(self):
    thisUID = os.getuid()
    cmdToExecute = 'echo "Hello"\newflkjdsfdsjlk\necho "Goodbye"'
    expResSTDOUT = 'Hello\n/bin/sh: 2: ewflkjdsfdsjlk: not found\nGoodbye\n'
    res = appObj.jobExecutor.executeCommand(SimpleJobExecutionClass(cmdToExecute))
    self.assertEqual(res.stdout.decode(), expResSTDOUT)

  def test_ExecuteAsDockJobUserUser(self):
    env = {
      'APIAPP_MODE': 'DOCKER',
      'APIAPP_VERSION': 'TEST-3.3.3',
      'APIAPP_FRONTEND': '../app',
      'APIAPP_APIURL': 'http://apiurlxxx:45/aa/bb/cc',
      'APIAPP_APIACCESSSECURITY': '[]',
      'APIAPP_USERFORJOBS': 'dockjobuser',
      'APIAPP_GROUPFORJOBS': 'dockjobgroup',
    }
    appObj.init(env, self.standardStartupTime)
    testClient = appObj.flaskAppObject.test_client()
    testClient.testing = True 

    cmdToExecute = 'whoami'
    expResSTDOUT = 'dockjobuser\n'
    res = appObj.jobExecutor.executeCommand(SimpleJobExecutionClass(cmdToExecute))
    self.assertEqual(res.stdout.decode(), expResSTDOUT)
    
    appObj.jobExecutor.stopThreadRunning()
    testClient = None



