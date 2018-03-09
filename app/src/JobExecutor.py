# JobExecutor objects will run a separate thread that will execute jobs
#  Jobs will be run as a separate user to the main user
import subprocess
import os
import signal
import pwd
import grp
import time

class JobExecutorClass():
  processUserID = None
  processGroupID = None
  timeout = 15 #default to 15 second timeout for jobs

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
    #completedProcess = subprocess.run(shellCmd, stdin=None, input=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, cwd=None, timeout=self.timeout, check=False, preexec_fn=self.getDemoteFunction())
    #return completedProcess
    start_time = time.time()
    proc = subprocess.Popen(shellCmd, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, cwd=None, preexec_fn=self.getDemoteFunction())
    returncode = None
    while (returncode == None):
      returncode = proc.poll()
      if (time.time() - start_time) > self.timeout:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        #valid return codes are between 0-255. I have hijacked -1 for timeout
        returncode = -1
      time.sleep(0.2)
    stdout, stderr = proc.communicate()
    completed = subprocess.CompletedProcess(
      args=shellCmd,
      returncode=returncode,
      stdout=stdout,
      stderr=stderr,
    )
    return completed

  def getDemoteFunction(self):
    def demote():
      # must set group first as user may not have permission to set group
      os.setgid(self.processGroupID)
      os.setuid(self.processUserID)
      # Set a session ID. When this process is killed I need to kill a program group (because I use Shell=True) and if 
      #  I don't set a session ID that will kill the server also
      # https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true/4791612#4791612
      os.setsid()
    return demote

