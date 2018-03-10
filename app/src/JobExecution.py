# JobExecution represents a single execution of a Job
import datetime
import pytz
import uuid
from subprocess import TimeoutExpired
from flask_restplus import fields


def getJobExecutionCreationModel(appObj):
  return appObj.flastRestPlusAPIObject.model('JobExecutionCreation', {
    'name': fields.String(default='')
  })

def getJobExecutionModel(appObj):
  return appObj.flastRestPlusAPIObject.model('JobExecution', {
    'guid': fields.String(default='',description='Unique identifier for this job execution'),
    'executionName': fields.String(default=''),
    'manual': fields.Boolean(default=False,description='Was the Job manually requested'),
    'stage': fields.String(default='',description='Execution Stage'),
    'jobGUID': fields.String(default='',description='Unique identifier for the job this execution is for'),
    'jobCommand': fields.String(default=''),
    'dateCreated': fields.DateTime(dt_format=u'iso8601', description='Time the execution was requested'),
    'dateStarted': fields.DateTime(dt_format=u'iso8601', description='Time the execution was started'),
    'dateCompleted': fields.DateTime(dt_format=u'iso8601', description='Time the execution was completed'),
    'resultReturnCode': fields.Integer(default=0,description='Return code or -1 for timed out'),
    'resultsSTDOUT': fields.String(default='',description='Output from the job'),
  })


class JobExecutionClass():
  guid = None
  executionName = None #executons not accessible by this name which dosen't have to be unique
  manual = None #manually ran or ran from schedule
  stage = None  #Pending, Running, Completed, Timeout
  jobGUID = None
  jobCommand = None
  dateCreated = None
  dateStarted = None
  dateCompleted = None
  resultReturnCode = None
  resultSTDOUT = None


  def __init__(self, job, executionName, manual):
    self.guid = str(uuid.uuid4())
    self.stage = 'Pending'
    self.jobGUID = job.guid
    self.jobCommand = job.command
    self.dateCreated = datetime.datetime.now(pytz.timezone("UTC")).isoformat()
    self.dateStarted = None
    self.dateCompleted = None
    self.resultReturnCode = None
    self.resultSTDOUT = None
    self.executionName = executionName
    self.manual = manual

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



