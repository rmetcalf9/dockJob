from TestHelperSuperClass import testHelperAPIClient
from JobExecutor import JobExecutorClass
from JobExecution import SimpleJobExecutionClass
import os
from appObj import appObj
import uuid
import pytest

@pytest.mark.executor
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
      'DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD': 'some_password',
      'APIAPP_TRIGGERAPIURL': 'http://triggerapiurlxxx'
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

  def test_use_cat_to_output_stdin(self):
    env = {
      'APIAPP_MODE': 'DOCKER',
      'APIAPP_VERSION': 'TEST-3.3.3',
      'APIAPP_FRONTEND': '../app',
      'APIAPP_APIURL': 'http://apiurlxxx:45/aa/bb/cc',
      'APIAPP_APIACCESSSECURITY': '[]',
      'APIAPP_USERFORJOBS': 'dockjobuser',
      'APIAPP_GROUPFORJOBS': 'dockjobgroup',
      'DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD': 'some_password',
      'APIAPP_TRIGGERAPIURL': 'http://triggerapiurlxxx'
    }
    appObj.init(env, self.standardStartupTime)
    testClient = appObj.flaskAppObject.test_client()
    testClient.testing = True

    example_stdin = 'aa\nbb\ncc\n£R$TGFFTY:::SAAS{}SDs'

    cmdToExecute = 'cat -'
    expResSTDOUT = example_stdin
    res = appObj.jobExecutor.executeCommand(SimpleJobExecutionClass(cmdToExecute, stdinData=example_stdin.encode('utf-8')))
    self.assertEqual(res.stdout.decode(), expResSTDOUT)

    appObj.jobExecutor.stopThreadRunning()
    testClient = None

  def test_cat_and_stdin_with_before_and_after(self):
    env = {
      'APIAPP_MODE': 'DOCKER',
      'APIAPP_VERSION': 'TEST-3.3.3',
      'APIAPP_FRONTEND': '../app',
      'APIAPP_APIURL': 'http://apiurlxxx:45/aa/bb/cc',
      'APIAPP_APIACCESSSECURITY': '[]',
      'APIAPP_USERFORJOBS': 'dockjobuser',
      'APIAPP_GROUPFORJOBS': 'dockjobgroup',
      'DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD': 'some_password',
      'APIAPP_TRIGGERAPIURL': 'http://triggerapiurlxxx'
    }
    appObj.init(env, self.standardStartupTime)
    testClient = appObj.flaskAppObject.test_client()
    testClient.testing = True

    example_stdin = 'aa\nbb\ncc\n£R$TGFFTY:::SAAS{}SDs'

    cmdToExecute = 'echo "START"\ncat -\necho "END"'
    expResSTDOUT = "START\n" + example_stdin + "END\n"
    res = appObj.jobExecutor.executeCommand(SimpleJobExecutionClass(cmdToExecute, stdinData=example_stdin.encode('utf-8')))
    self.assertEqual(res.stdout.decode(), expResSTDOUT)

    appObj.jobExecutor.stopThreadRunning()
    testClient = None

  def test_job_gets_stdin_but_ignores_it(self):
    env = {
      'APIAPP_MODE': 'DOCKER',
      'APIAPP_VERSION': 'TEST-3.3.3',
      'APIAPP_FRONTEND': '../app',
      'APIAPP_APIURL': 'http://apiurlxxx:45/aa/bb/cc',
      'APIAPP_APIACCESSSECURITY': '[]',
      'APIAPP_USERFORJOBS': 'dockjobuser',
      'APIAPP_GROUPFORJOBS': 'dockjobgroup',
      'DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD': 'some_password',
      'APIAPP_TRIGGERAPIURL': 'http://triggerapiurlxxx'
    }
    appObj.init(env, self.standardStartupTime)
    testClient = appObj.flaskAppObject.test_client()
    testClient.testing = True

    example_stdin = 'aa\nbb\ncc\n£R$TGFFTY:::SAAS{}SDs'

    cmdToExecute = 'echo "I have stdin but I am not going to read it"'
    expResSTDOUT = "I have stdin but I am not going to read it\n"
    res = appObj.jobExecutor.executeCommand(SimpleJobExecutionClass(cmdToExecute, stdinData=example_stdin.encode('utf-8')))
    self.assertEqual(res.stdout.decode(), expResSTDOUT)

    appObj.jobExecutor.stopThreadRunning()
    testClient = None