from TestHelperSuperClass import testHelperAPIClient
from JobExecutor import JobExecutorClass
import os
from appObj import appObj

class test_appObjClass(testHelperAPIClient):

  def test_ExecutorConstructor(self):
    pass

  def test_ExecuteAsThisUser(self):
    thisUID = os.getuid()
    thisGID = os.getgid()
    cmdToExecute = 'id -u'
    expResSTDOUT = str(thisUID) + '\n'
    res = appObj.jobExecutor.executeCommand(cmdToExecute)
    self.assertEqual(res.stdout.decode(), expResSTDOUT)

  def test_ErrorSTDErrOutput(self):
    thisUID = os.getuid()
    thisGID = os.getgid()
    cmdToExecute = 'sadgfdhgf'
    expResSTDOUT = '/bin/sh: 1: sadgfdhgf: not found\n'
    res = appObj.jobExecutor.executeCommand(cmdToExecute)
    self.assertEqual(res.stdout.decode(), expResSTDOUT)

  def test_MultipleCommandsWithMixedOutput(self):
    thisUID = os.getuid()
    thisGID = os.getgid()
    cmdToExecute = 'echo "Hello"\newflkjdsfdsjlk\necho "Goodbye"'
    expResSTDOUT = 'Hello\n/bin/sh: 2: ewflkjdsfdsjlk: not found\nGoodbye\n'
    res = appObj.jobExecutor.executeCommand(cmdToExecute)
    self.assertEqual(res.stdout.decode(), expResSTDOUT)
