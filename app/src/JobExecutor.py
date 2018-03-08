# JobExecutor objects will run a separate thread that will execute jobs
#  Jobs will be run as a separate user to the main user
import subprocess
import os
import pwd
import grp

class JobExecutorClass():
  processUserID = None
  processGroupID = None

  def __init__(self, appObj):
    if os.getuid() != 0:
      raise Exception('Job Executor only works when run as root')
    if appObj.userforjobs == None:
      raise Exception('No user set')

    try:
      self.processUserID = pwd.getpwnam(appObj.userforjobs).pw_uid
    except:
      raise Exception('Could not find user id for ' + appObj.userforjobs)
    groupent = None
    try:
      groupent = grp.getgrnam(appObj.groupforjobs)
      self.processGroupID = groupent.gr_gid
    except:
      raise Exception('Could not find group id for ' + appObj.groupforjobs)
    if not appObj.userforjobs == 'root':
      if not appObj.userforjobs in groupent.gr_mem:
        print(groupent.gr_mem)
        raise Exception('User ' + appObj.userforjobs + ' is not in group ' + appObj.groupforjobs)
    
    print('Will run jobs as user: ' + appObj.userforjobs + ' (' + str(self.processUserID) + ')')
    print('Will run jobs as group: ' + appObj.groupforjobs + ' (' + str(self.processGroupID) + ')')

    testProcess = self.executeCommand('whoami')
    if testProcess.returncode != 0:
      print(testProcess.stdout.decode())
      if testProcess.stderr != None:
        print(testProcess.stderr.decode())
      raise Exception('Test process didn''t return success. returncode = ' + testProcess.returncode)
    if testProcess.stdout.decode().strip() != appObj.userforjobs:
      print(testProcess.stdout.decode())
      if testProcess.stderr != None:
        print(testProcess.stderr.decode())
      raise Exception('Test process running as wrong user')
    print('Test process passed')

  #Function to execute the command. Passed the shell string and outputs the executed result
  def executeCommand(self, shellCmd):
    # https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess
    completedProcess = subprocess.run(shellCmd, stdin=None, input=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, cwd=None, timeout=None, check=False, preexec_fn=self.getDemoteFunction())
    return completedProcess

  def getDemoteFunction(self):
    def demote():
      # must set group first as user may not have permission to set group
      os.setgid(self.processGroupID)
      os.setuid(self.processUserID)
    return demote

