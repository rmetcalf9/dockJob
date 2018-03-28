from flask import request
from flask_restplus import Resource, fields, apidoc
from werkzeug.exceptions import BadRequest
import uuid
import json
import datetime
# from pytz import timezone
import pytz
from RepetitionInterval import RepetitionIntervalClass
from JobExecution import getJobExecutionCreationModel, getJobExecutionModel

#I need jobs to be stored in order so pagination works
from sortedcontainers import SortedDict

jobModel = None
def getJobModel(appObj):
  global jobModel
  if jobModel is None:
    jobModel = appObj.flastRestPlusAPIObject.model('Job', {
      'name': fields.String(default=''),
      'command': fields.String(default=''),
      'enabled': fields.Boolean(default=False,description='Is the job currently enabled'),
      'repetitionInterval': fields.String(default='',description='How the job is scheduled to run'),
      'nextScheduledRun': fields.String(default='',description='Next scheudled run'),
      'guid': fields.String(default='',description='Unique identifier for this job'),
      'creationDate': fields.DateTime(dt_format=u'iso8601', description='Time job record was created'),
      'lastUpdateDate': fields.DateTime(dt_format=u'iso8601', description='Last time job record was changed (excluding runs)'),
      'lastRunDate': fields.DateTime(dt_format=u'iso8601', description='Last time job record was run'),
      'lastRunReturnCode': fields.Integer(default=None,description='Return code for the last execution of this job or -1 for timed out'),
      'lastRunExecutionGUID': fields.String(default='',description='Unique identifier for the last job execution for this job')
    })
  return jobModel


def getJobServerInfoModel(appObj):
  return appObj.flastRestPlusAPIObject.model('ServerInfoJobs', {
    'TotalJobs': fields.Integer(default='0',description='Total Jobs'),
    'NextJobsToExecute': fields.List(fields.Nested(getJobModel(appObj)))
  })

def uniqueJobName(name):
  return name.strip().upper()

#Class to represent a job
class jobClass():
  guid = None
  name = None
  command = None
  enabled = None
  repetitionInterval = None
  creationDate = None
  lastUpdateDate = None
  lastRunDate = None
  nextScheduledRun = None
  lastRunReturnCode = None
  lastRunExecutionGUID = None

  def __repr__(self):
    ret = 'jobClass('
    ret += 'guid:' + self.guid + ' '
    ret += 'name:' + self.name + ' '
    ret += 'command:' + self.command + ' '
    ret += 'enabled:' + str(self.enabled) + ' '
    ret += 'repetitionInterval:' + self.repetitionInterval + ' '
    ret += 'creationDate:' + self.creationDate
    ret += ')'
    return ret


  def __init__(self, name, command, enabled, repetitionInterval):
    if (len(name)<2):
      raise BadRequest('Job name must be more than 2 characters')
    curTime = datetime.datetime.now(pytz.timezone("UTC"))
    self.guid = str(uuid.uuid4())
    self.name = name
    self.command = command
    self.enabled = enabled
    self.repetitionInterval = repetitionInterval
    self.creationDate = curTime.isoformat()
    self.lastUpdateDate = curTime.isoformat()
    self.lastRunDate = None
    self.lastRunExecutionGUID = ''
    self.lastRunReturnCode = None

    self.setNextScheduledRun(datetime.datetime.now(pytz.timezone("UTC")))


  def setNextScheduledRun(self, curTime):
    ri = None
    if (self.repetitionInterval != None):
      if (self.repetitionInterval != ''):
        try:
          ri = RepetitionIntervalClass(self.repetitionInterval)
        except:
          raise BadRequest('Invalid Repetition Interval')
        ri = RepetitionIntervalClass(self.repetitionInterval)
        self.nextScheduledRun = ri.getNextOccuranceDatetime(curTime).isoformat()

  def uniqueName(self):
    return uniqueJobName(self.name)

class jobsDataClass():
  # map of guid to Job
  jobs = None
  # map of Job name to guid
  jobs_name_lookup = None
  appObj = None

  def __init__(self, appObj):
    self.jobs = SortedDict()
    self.jobs_name_lookup = SortedDict()
    self.appObj = appObj

  def getJobServerInfo(self):
    nextJobToExecute = self.getNextJobToExecute()
    if nextJobToExecute is None:
      xx = []
    else:
      xx = [nextJobToExecute]
    return{
      'TotalJobs': len(self.jobs),
      'NextJobsToExecute': xx
    }
    
  def getJob(self, guid):
    try:
      r = self.jobs[str(guid)]
    except KeyError:
      raise BadRequest('Invalid Job GUID')
    return r
  def getJobByName(self, name):
    return self.jobs[str(self.jobs_name_lookup[uniqueJobName(name)])]

  # return GUID or error
  def addJob(self, job):
    uniqueJobName = job.uniqueName()
    if (str(job.guid) in self.jobs):
      return {'msg': 'GUID already in use', 'guid':''}
    if (uniqueJobName in self.jobs_name_lookup):
      return {'msg': 'Job Name already in use - ' + uniqueJobName, 'guid':''}
    self.jobs[str(job.guid)] = job
    self.jobs_name_lookup[uniqueJobName] = job.guid
    self.nextJobToExecuteCalcRequired = True
    return {'msg': 'OK', 'guid':job.guid}

  def deleteJob(self, jobObj):
    uniqueJobName = jobObj.uniqueName()
    tmpVar = self.jobs_name_lookup.pop(uniqueJobName)
    if tmpVar is None:
      raise Execption('Failed to delete a job could not get it out of the job name lookup')
    tmpVar2 = self.jobs.pop(jobObj.guid)
    if tmpVar2 is None:
      raise Execption('Failed to delete a job could not get it out of the jobs')
    # Delete any executions
    self.appObj.jobExecutor.deleteExecutionsForJob(jobObj.guid)
    # If it is next to execute we need to recaculate
    if self.nextJobToExecute != None:
      if jobObj.guid == self.nextJobToExecute.guid:
        self.nextJobToExecuteCalcRequired = True

  #nextJobToExecute holds the next job scheduled to execute
  # When ever any actions are preformed that may change this the CalcRequired flag is set to true
  # the get function will either return or recaculate as desired
  # Changing actions:
  #  - Adding Job
  #  - Delete job if it is the next to execute
  #  - Executing a job
  # None is a valid next job to execute but when it 
  nextJobToExecute = None
  nextJobToExecuteCalcRequired = True
  def getNextJobToExecute(self):
    if not self.nextJobToExecuteCalcRequired:
      return self.nextJobToExecute
    self.nextJobToExecute = None
    for jobIdx in self.jobs:
      if self.jobs[jobIdx].nextScheduledRun is not None:
        if self.nextJobToExecute is None:
          self.nextJobToExecute = self.jobs[jobIdx]
        else:
          if self.jobs[jobIdx].nextScheduledRun < self.nextJobToExecute.nextScheduledRun:
            self.nextJobToExecute = self.jobs[jobIdx]
    self.nextJobToExecuteCalcRequired = False
    return self.nextJobToExecute

  def registerRunDetails(self, jobGUID, newLastRunDate, newLastRunReturnCode, newLastRunExecutionGUID):
    self.jobs[str(jobGUID)].lastRunDate = newLastRunDate
    self.jobs[str(jobGUID)].lastRunReturnCode = newLastRunReturnCode
    self.jobs[str(jobGUID)].lastRunExecutionGUID = newLastRunExecutionGUID

  #funciton for testing allowing us to pretend it is currently a different time
  def recaculateExecutionTimesBasedonNewTime(self, curTime):
    for jobIdx in self.jobs:
      self.jobs[jobIdx].setNextScheduledRun(curTime)
    self.nextJobToExecuteCalcRequired = True


def resetData(appObj):
  appObj.appData['jobsData']=jobsDataClass(appObj)

def registerAPI(appObj):
  # Fields required to create a Job
  jobCreationModel = appObj.flastRestPlusAPIObject.model('JobCreation', {
    'name': fields.String(default=''),
    'command': fields.String(default=''),
    'enabled': fields.Boolean(default=False,description='Is the job currently enabled'),
    'repetitionInterval': fields.String(default='',description='How the job is scheduled to run'),
  })

  nsJobs = appObj.flastRestPlusAPIObject.namespace('jobs', description='Job Operations')
  @nsJobs.route('/')
  class jobList(Resource):
    '''Operations relating to jobs'''

    @nsJobs.doc('getjobs')
    @nsJobs.marshal_with(appObj.getResultModel(getJobModel(appObj)))
    @appObj.flastRestPlusAPIObject.response(200, 'Success')
    @nsJobs.param('offset', 'Number to start from')
    @nsJobs.param('pagesize', 'Results per page')
    @nsJobs.param('query', 'Search Filter')
    def get(self):
      '''Get Jobs'''
      def outputJob(item):
        return appObj.appData['jobsData'].jobs[item]
      def filterJob(item, whereClauseText): #if multiple separated by spaces each is passed individually and anded together
        if appObj.appData['jobsData'].jobs[item].name.upper().find(whereClauseText) != -1:
          return True
        if appObj.appData['jobsData'].jobs[item].command.upper().find(whereClauseText) != -1:
          return True
        return False
      return appObj.getPaginatedResult(
        appObj.appData['jobsData'].jobs_name_lookup,
        outputJob,
        request,
        filterJob
      )

    @nsJobs.doc('postjob')
    @nsJobs.expect(jobCreationModel, validate=True)
    @appObj.flastRestPlusAPIObject.response(400, 'Validation error')
    @appObj.flastRestPlusAPIObject.response(200, 'Success')
    @appObj.flastRestPlusAPIObject.marshal_with(getJobModel(appObj), code=200, description='Job created')
    def post(self):
      '''Create Job'''
      content = request.get_json()
      jobObj = jobClass(content['name'], content['command'], content['enabled'], content['repetitionInterval'])
      res = appObj.appData['jobsData'].addJob(jobObj)
      if res['msg']!='OK':
        raise BadRequest(res['msg'])
      return appObj.appData['jobsData'].getJob(res['guid'])

  @nsJobs.route('/<string:guid>')
  @nsJobs.response(400, 'Job not found')
  @nsJobs.param('guid', 'Job identifier (or name)')
  class job(Resource):
    '''Show a single Job'''
    @nsJobs.doc('get_job')
    @nsJobs.marshal_with(getJobModel(appObj))
    def get(self, guid):
      '''Fetch a given resource'''
      try:
        return appObj.appData['jobsData'].getJob(guid).__dict__
      except:
        try:
          return appObj.appData['jobsData'].getJobByName(guid).__dict__
        except:
          raise BadRequest('Invalid Job Identifier')
      return None

    @nsJobs.doc('delete_job')
    @nsJobs.response(200, 'Job deleted')
    @nsJobs.response(400, 'Job not found')
    def delete(self, guid):
      '''Delete job'''
      deletedJob = None
      try:
        deletedJob = appObj.appData['jobsData'].getJob(guid)
      except:
        try:
          deletedJob = appObj.appData['jobsData'].getJobByName(guid)
        except:
          raise BadRequest('Invalid Job Identifier')
      appObj.appData['jobsData'].deleteJob(deletedJob)
      return deletedJob.__dict__

  @nsJobs.route('/<string:guid>/execution')
  @nsJobs.response(400, 'Job not found')
  @nsJobs.param('guid', 'Job identifier (or name)')
  class jobExecutionList(Resource):
    @nsJobs.doc('postexecution')
    @nsJobs.expect(getJobExecutionCreationModel(appObj), validate=True)
    @appObj.flastRestPlusAPIObject.response(400, 'Validation error')
    @appObj.flastRestPlusAPIObject.response(200, 'Success')
    @appObj.flastRestPlusAPIObject.marshal_with(getJobExecutionModel(appObj), code=200, description='Job created')
    def post(self, guid):
      '''Create Job Execution'''
      content = request.get_json()
      return appObj.jobExecutor.submitJobForExecution(guid, content['name'], True)

    @nsJobs.doc('getjobexecutions')
    @nsJobs.marshal_with(appObj.getResultModel(getJobExecutionModel(appObj)))
    @appObj.flastRestPlusAPIObject.response(200, 'Success')
    @nsJobs.param('offset', 'Number to start from')
    @nsJobs.param('pagesize', 'Results per page')
    @nsJobs.param('query', 'Search Filter')
    def get(self, guid):
      '''Get Job Executions'''
      def outputJobExecution(item):
        return item
      def filterJobExecution(item, whereClauseText): #if multiple separated by spaces each is passed individually and anded together
        return True
      return appObj.getPaginatedResult(
        appObj.jobExecutor.getAllJobExecutions(guid),
        outputJobExecution,
        request,
        filterJobExecution
      )


