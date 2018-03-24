# JobExecutor objects will run a separate thread that will execute jobs
#  Jobs will be run as a separate user to the main user
import subprocess
import os
import signal
import pwd
import grp
import time
import threading
from JobExecution import JobExecutionClass
from sortedcontainers import SortedDict
import datetime
import pytz
import queue
from utils import from_iso8601

class JobExecutorClass(threading.Thread):
  processUserID = None
  processGroupID = None
  timeout = 15 #default to 15 second timeout for jobs
  appObj = None

  # https://docs.python.org/3/library/asyncio-sync.html#asyncio.Lock
  JobExecutions =  None
  JobExecutionLock = None
  pendingExecutions = None # Queue to hold GUID's of executions to run

  def __init__(self, appObj, skipUserCheck):
    self.JobExecutions =  SortedDict()
    self.JobExecutionLock = threading.Lock()
    self.pendingExecutions = queue.Queue() # Queue to hold GUID's of executions to run
    self.appObj = appObj
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

    if not skipUserCheck:
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
      print('User check passed')

    threading.Thread.__init__(self)
    #super(threading.Thread, self).__init__()

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

  #Making this a function to set default params
  def aquireJobExecutionLock(self):
    if not self.JobExecutionLock.acquire(blocking=True, timeout=0.5): #timeout value is in seconds
      raise Exception("Timedout waiting for lock")
    
  #called when new service needs submission
  def submitJobForExecution(self, jobGUID, executionName, manual):
    #manual = True when called by jobsDataAPI and False when called from scheduler
    jobObj = self.appObj.appData['jobsData'].getJob(jobGUID)
    if jobObj is None:
      raise BadRequest('Invalid job')
    execution = JobExecutionClass(jobObj, executionName, manual)
    #lock shouldn't be needed but it is a cheap operation
    try:
      self.aquireJobExecutionLock()
      self.JobExecutions[execution.guid] = execution
    finally:
      self.JobExecutionLock.release()
    self.pendingExecutions.put(execution.guid)
    return execution

  def deleteExecutionsForJob(self, jobGUID):
    executionsToDelete = queue.Queue()
    for cur in self.JobExecutions:
      if self.JobExecutions[cur].jobGUID == jobGUID:
        executionsToDelete.put(cur)

    while not executionsToDelete.empty():
      toDel = executionsToDelete.get()
      self.deleteExecution(self.JobExecutions[toDel].guid)


  def deleteExecution(self, executionGUID):
   try:
     self.aquireJobExecutionLock()
     tmpVar = self.JobExecutions.pop(executionGUID)
     if tmpVar is None:
       raise Execption('Failed to delete a job execution - could not get it out of the job name lookup')
   finally:
     self.JobExecutionLock.release()

  #return current data for a job execution
  def getJobExecutionStatus(self, jobGUID):
    try:
      return self.JobExecutions[jobGUID]
    except KeyError:
      return None
    return retVal
  
  #return all the jobs, if jobGUID is none than all, otherwise filter just for that job
  def getAllJobExecutions(self, jobGUID):
    output = SortedDict()
    try:
      self.aquireJobExecutionLock()
      for cur in self.JobExecutions:
        if jobGUID is None:
          output[self.JobExecutions[cur].guid] = self.JobExecutions[cur]
        else:
          if jobGUID == self.JobExecutions[cur].jobGUID:
            output[self.JobExecutions[cur].guid] = self.JobExecutions[cur]
    finally:
      self.JobExecutionLock.release()
    return output

  def loopIteration(self, curDatetime):
    #Run next pending job only the next one, other jobs are run on subsequent loop iterations
    # this will block this thread until the execution is complete
    if not self.pendingExecutions.empty():
      executionGUID = self.pendingExecutions.get()
      jobExecutionObj = None
      try:
        jobExecutionObj = self.JobExecutions[executionGUID]
      except KeyError:
        jobExecutionObj = None # if we get a key error it just means this job was deleted while it had a pending execution
      if jobExecutionObj is not None:
        print('Executing ' + jobExecutionObj.executionName)
        jobExecutionObj.execute(self.appObj.jobExecutor, self.JobExecutionLock)

    #schedule any new jobs that are due to be automatically run
    #  no lock acquire required here as it is inside submitJobForExecution
    nextJob = self.appObj.appData['jobsData'].getNextJobToExecute()
    if nextJob is not None:
      if curDatetime.isoformat() > nextJob.nextScheduledRun:
        # print('Submitting job ' + nextJob.name + ' for scheduled execution')
        self.submitJobForExecution(nextJob.guid, '', False)
        nextJob.setNextScheduledRun(curDatetime)
        self.appObj.appData['jobsData'].nextJobToExecuteCalcRequired = True

    #purge old runs from list
    timeToPurgeBefore = curDatetime - datetime.timedelta(days=7)
    toPurge = queue.Queue()
    try:
      self.aquireJobExecutionLock()
      for curJobExecution in self.JobExecutions:
        if self.JobExecutions[curJobExecution].dateCompleted is not None:
          if from_iso8601(self.JobExecutions[curJobExecution].dateCompleted) < timeToPurgeBefore:
            toPurge.put(curJobExecution)
      while not toPurge.empty():
        toDel = toPurge.get()
        self.JobExecutions.pop(toDel)
    finally:
      self.JobExecutionLock.release()

  #main loop of thread
  running = True
  def run(self):
    self.running = True
    print('Job runner thread starting')
    while self.running:
      curDatetime = datetime.datetime.now(pytz.utc)
      self.loopIteration(curDatetime)
      time.sleep(0.2)
    print('Job runner thread terminating')

  def stopThreadRunning(self):
    self.running = False
    #not sleeping here in case appObj has other threads to stop. (Should stop them all then wait once)
    #time.sleep(0.3) #give thread a chance to stop
