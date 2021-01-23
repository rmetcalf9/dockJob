# JobExecution represents a single execution of a Job
import datetime
import pytz
import uuid
from subprocess import TimeoutExpired
from flask_restx import fields

JobExecutionCreationModel = None
def getJobExecutionCreationModel(appObj):
  global JobExecutionCreationModel
  if JobExecutionCreationModel is None:
    JobExecutionCreationModel = appObj.flastRestPlusAPIObject.model('JobExecutionCreation', {
    'name': fields.String(default='')
  })
  return JobExecutionCreationModel

def getJobExecutionModel(appObj):
  return appObj.flastRestPlusAPIObject.model('JobExecution', {
    'guid': fields.String(default='',description='Unique identifier for this job execution'),
    'executionName': fields.String(default=''),
    'manual': fields.Boolean(default=False,description='Was the Job manually requested'),
    'stage': fields.String(default='',description='Execution Stage'),
    'jobGUID': fields.String(default='',description='Unique identifier for the job this execution is for'),
    'jobName': fields.String(default='',description='Name of the job being executed'),
    'jobCommand': fields.String(default=''),
    'dateCreated': fields.DateTime(dt_format=u'iso8601', description='Time the execution was requested'),
    'dateStarted': fields.DateTime(dt_format=u'iso8601', description='Time the execution was started'),
    'dateCompleted': fields.DateTime(dt_format=u'iso8601', description='Time the execution was completed'),
    'resultReturnCode': fields.Integer(default=0,description='Return code or -1 for timed out'),
    'resultSTDOUT': fields.String(default='',description='Output from the job')
  })


#Simple execution object with subset of features
# it allows the jobExecutor.executeCommand fn to be called
# this is used for the initial startup test and for unit testing
#this is never setup as an actual job
class SimpleJobObj():
  name = 'SimpleJobObjConstantName'
  guid = None
  def __init__(self):
    self.guid = str(uuid.uuid4())

class SimpleJobExecutionClass():
  guid = None
  executionName = None 
  manual = None 
  stage = None  
  jobGUID = None
  jobCommand = None
  dateCreated = None
  dateStarted = None
  dateCompleted = None
  resultReturnCode = None
  resultSTDOUT = None

  #Items not in JSON output
  jobObj = None
  triggerJobObj = None
  triggerExecutionObj = None


  def __init__(self, command):
    self.guid = str(uuid.uuid4())
    self.jobCommand = command
    self.jobObj = SimpleJobObj()
    self.jobGUID = self.jobObj.guid
    self.triggerJobObj = None
    self.triggerExecutionObj = None
    self.executionName = 'SimpleJobExecutionConstantName'

  def getJobExecutionMethod(self):
    return 'Manual'

  def _caculatedDict(self):
    ret = dict(self.__dict__)
    ret['jobName'] = self.jobObj.name
    del ret['jobObj']
    del ret['triggerJobObj']
    del ret['triggerExecutionObj']
    return ret



class JobExecutionClass():
  guid = None
  executionName = None #executons not accessible by this name which dosen't have to be unique
  manual = None #manually ran or ran from schedule
  stage = None  #Pending, Running, Completed, Timeout
  jobGUID = None #copy taken on init so it is invariant during execution
  jobCommand = None #copy taken on init so it is invariant during execution
  dateCreated = None
  dateStarted = None
  dateCompleted = None
  resultReturnCode = None
  resultSTDOUT = None

  #Items not in JSON output
  jobObj = None
  triggerJobObj = None
  triggerExecutionObj = None

  def __repr__(self):
    ret = 'JobExecutionClass('
    ret += 'guid:' + self.guid + ' '
    ret += 'executionName:' + self.executionName + ' '
    ret += 'manual:' + str(self.manual) + ' '
    ret += 'stage:' + self.stage + ' '
    ret += 'jobGUID:' + self.jobGUID + ' '
    ret += 'jobCommand:' + self.jobCommand + ' '
    ret += 'dateCreated:' + self.dateCreated + ' '
    ret += 'dateStarted:' + str(self.dateStarted) + ' '
    ret += 'dateCompleted:' + str(self.dateCompleted) + ' '
    ret += 'resultReturnCode:' + str(self.resultReturnCode) + ' '
    ret += 'resultSTDOUT:' + str(self.resultSTDOUT)
    ret += ')'
    return ret


  def __init__(self, jobObj, executionName, manual, curDatetime, triggerJobObj, triggerExecutionObj):
    self.guid = str(uuid.uuid4())
    self.stage = 'Pending'
    self.jobGUID = jobObj.guid
    self.jobCommand = jobObj.command
    self.dateCreated = curDatetime.isoformat()
    self.dateStarted = None
    self.dateCompleted = None
    self.resultReturnCode = None
    self.resultSTDOUT = None
    self.executionName = executionName
    self.manual = manual
    self.jobObj = jobObj
    self.triggerJobObj = triggerJobObj
    self.triggerExecutionObj = triggerExecutionObj

  def _caculatedDict(self):
    ret = dict(self.__dict__)
    ret['jobName'] = self.jobObj.name
    del ret['jobObj']
    del ret['triggerJobObj']
    del ret['triggerExecutionObj']
    return ret

  def execute(self, executor, lockAcquireFn, lockReleaseFn, registerRunDetailsFn, appObj):
    lockAcquireFn()
    self.stage = 'Running'
    self.dateStarted = appObj.getCurDateTime().isoformat()
    ##I only want to register the run when it completes because then I can record it's result and fire any events
    ##registerRunDetailsFn(jobGUID=self.jobGUID, newLastRunDate=appObj.getCurDateTime(), newLastRunReturnCode=None, triggerExecutionObj=self)
    lockReleaseFn()
    try:
      executionResult = executor.executeCommand(self)
    except TimeoutExpired:
      lockAcquireFn()
      self.resultReturnCode = -1
      self.resultSTDOUT = None
      self.stage = 'Timeout'
      self.dateCompleted = appObj.getCurDateTime().isoformat()
      registerRunDetailsFn(jobGUID=self.jobGUID, newLastRunDate=appObj.getCurDateTime(), newLastRunReturnCode=self.resultReturnCode, triggerExecutionObj=self)
      lockReleaseFn()
      return
    lockAcquireFn()
    self.resultReturnCode = executionResult.returncode
    try:
      self.resultSTDOUT = executionResult.stdout.decode().strip()
    except Exception:
      self.resultSTDOUT = "ERROR - failed to decode output probally because it wasn't in utf-8 format"
    #valid exit codes are between 0-255. I have hijacked -1 for timeout
    if executionResult.returncode == -1:
      self.stage = 'Timeout'
    else:
      self.stage = 'Completed'
    self.dateCompleted = appObj.getCurDateTime().isoformat()
    registerRunDetailsFn(jobGUID=self.jobGUID, newLastRunDate=appObj.getCurDateTime(), newLastRunReturnCode=self.resultReturnCode, triggerExecutionObj=self)
    lockReleaseFn()

  def getJobExecutionMethod(self):
    #determine setting from Manual,Scheduled,StateChangeToSuccess,StateChangeToFail,StateChangeToUnknown
    if self.manual:
      return 'Manual'
    if self.triggerJobObj is None:
      return 'Scheduled'
    return 'StateChangeTo' + self.triggerJobObj.mostRecentCompletionStatus

