# JobExecution represents a single execution of a Job
import datetime
import pytz
import uuid
from subprocess import TimeoutExpired

class JobExecutionClass():
  guid = None
  stage = None  #Pending, Running, Completed, Timeout
  jobGUID = None
  jobCommand = None
  dateCreated = None
  dateStarted = None
  dateCompleted = None
  resultReturnCode = None
  resultSTDOUT = None


  def __init__(self, job):
    self.guid = str(uuid.uuid4())
    self.stage = 'Pending'
    self.jobGUID = job.guid
    self.jobCommand = job.command
    self.dateCreated = datetime.datetime.now(pytz.timezone("UTC")).isoformat()
    self.dateStarted = None
    self.dateCompleted = None
    self.resultReturnCode = None
    self.resultSTDOUT = None

  def execute(self, executor):
    self.stage = 'Running'
    self.dateStarted = datetime.datetime.now(pytz.timezone("UTC")).isoformat()
    try:
      executionResult = executor.executeCommand(self.jobCommand)
    except TimeoutExpired:
      self.resultReturnCode = -1
      self.resultSTDOUT = None
      self.stage = 'Timeout'
      self.dateCompleted = datetime.datetime.now(pytz.timezone("UTC")).isoformat()
      return
    self.resultReturnCode = executionResult.returncode
    self.resultSTDOUT = executionResult.stdout.decode().strip()
    #valid exit codes are between 0-255. I have hijacked -1 for timeout
    if executionResult.returncode == -1:
      self.stage = 'Timeout'
    else:
      self.stage = 'Completed'
    self.dateCompleted = datetime.datetime.now(pytz.timezone("UTC")).isoformat()
