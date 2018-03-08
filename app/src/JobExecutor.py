# JobExecutor objects will run a separate thread that will execute jobs
#  Jobs will be run as a separate user to the main user
import subprocess

class JobExecutorClass():
  processUserID = None
  processGroupID = None

  def __init__(self, processUserID, processGroupID):
    self.processUserUD = processUserID
    self.processGroupID = processGroupID

  #Function to execute the command. Passed the shell string and outputs the executed result
  def executeCommand(self, shellCmd):
    # https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess
    completedProcess = subprocess.run(shellCmd, stdin=None, input=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, cwd=None, timeout=None, check=False)
    return completedProcess
