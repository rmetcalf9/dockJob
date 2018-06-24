from flask import request
from flask_restplus import Resource, fields, apidoc
from werkzeug.exceptions import BadRequest
import uuid
import json
import datetime
import pytz
from JobExecution import getJobExecutionCreationModel, getJobExecutionModel
import enum
from jobObj import jobClass

#I need jobs to be stored in order so pagination works
from sortedcontainers import SortedDict

jobModel = None
def getJobModel(appObj):
  global jobModel
  if jobModel is None:
    jobModel = appObj.flastRestPlusAPIObject.model('Job', {
      'name': fields.String(default=''),
      'command': fields.String(default=''),
      'enabled': fields.Boolean(default=False,description='Is auto scheduling enabled - otherwise manual run only'),
      'repetitionInterval': fields.String(default='',description='How the job is scheduled to run'),
      'nextScheduledRun': fields.DateTime(dt_format=u'iso8601', description='Next scheudled run'),
      'guid': fields.String(default='',description='Unique identifier for this job'),
      'creationDate': fields.DateTime(dt_format=u'iso8601', description='Time job record was created'),
      'lastUpdateDate': fields.DateTime(dt_format=u'iso8601', description='Last time job record was changed (excluding runs)'),
      'lastRunDate': fields.DateTime(dt_format=u'iso8601', description='Last time job record was run'),
      'lastRunReturnCode': fields.Integer(default=None,description='Return code for the last execution of this job or -1 for timed out'),
      'lastRunExecutionGUID': fields.String(default='',description='Unique identifier for the last job execution for this job'),
      'mostRecentCompletionStatus': fields.String(default='Unknown',description='READONLY - Success, Fail or Unknown. Success or Fail if the job has run in last 25 hours, Unknown otherwise'),
      'pinned': fields.Boolean(default=False,description='Pin job to dashboard'),
      'overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown': fields.Integer(default=None,description='Override global number of minutes a job has not been run before a job is considered to have Unknown status for this job.'),
      'StateChangeSuccessJobGUID': fields.String(default=None,description='GUID of job to call when this jobs state changes to Success'),
      'StateChangeFailJobGUID': fields.String(default=None,description='GUID of job to call when this jobs state changes to Fail'),
      'StateChangeUnknownJobGUID': fields.String(default=None,description='GUID of job to call when this jobs state changes to Unknown'),
      'StateChangeSuccessJobNAME': fields.String(default=None,description='READONLY - Name of job to call when this jobs state changes to Success'),
      'StateChangeFailJobNAME': fields.String(default=None,description='READONLY - Name of job to call when this jobs state changes to Fail'),
      'StateChangeUnknownJobNAME': fields.String(default=None,description='READONLY - Name of job to call when this jobs state changes to Unknown'),
    })
  return jobModel

#Fields required when creating a job (A subset of the JobModel)
def getJobCreationModel(appObj):
  return appObj.flastRestPlusAPIObject.model('JobCreation', {
    'name': fields.String(default=''),
    'command': fields.String(default=''),
    'enabled': fields.Boolean(default=False,description='Is the job currently enabled'),
    'repetitionInterval': fields.String(default='',description='How the job is scheduled to run'),
    'pinned': fields.Boolean(default=False,description='Pin job to dashboard'),
    'overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown': fields.Integer(default=None,description='Override global number of minutes a job has not been run before a job is considered to have Unknown status for this job. (0 for no override)'),
    'StateChangeSuccessJobGUID': fields.String(default=None,description='GUID of job to call when this jobs state changes to Success'),
    'StateChangeFailJobGUID': fields.String(default=None,description='GUID of job to call when this jobs state changes to Fail'),
    'StateChangeUnknownJobGUID': fields.String(default=None,description='GUID of job to call when this jobs state changes to Unknown'),
  })

def getJobServerInfoModel(appObj):
  return appObj.flastRestPlusAPIObject.model('ServerInfoJobs', {
    'TotalJobs': fields.Integer(default='0',description='Total Jobs'),
    'NextJobsToExecute': fields.List(fields.Nested(getJobModel(appObj))),
    'JobsNeverRun': fields.Integer(default='-1',description='Jobs Never Run'),
    'JobsCompletingSucessfully': fields.Integer(default='-1',description='Jobs Completing Sucessfully'),
    'JobsLastExecutionFailed': fields.Integer(default='-1',description='Jobs where last execution failed')
  })

class jobsDataClass():
  # map of Jobs keyed by GUID
  jobs = None
  # map of Job name to guid
  jobs_name_lookup = None
  appObj = None

  def __init__(self, appObj):
    self.jobs = SortedDict()
    self.jobs_name_lookup = SortedDict()
    self.appObj = appObj

  #Run Job loop iteration
  def loopIteration(self, appObj, curTime):
    for jobIdx in self.jobs:
      self.jobs[jobIdx].loopIteration(appObj, curTime)

  def getJobServerInfo(self):
    nextJobToExecute = self.getNextJobToExecute()

    # Find Job stats
    JobsNeverRun = 0
    JobsCompletingSucessfully = 0
    JobsLastExecutionFailed = 0
    for jobIdx in self.jobs:
      if self.jobs[jobIdx].lastRunReturnCode is None:
        JobsNeverRun += 1
      else:
        if self.jobs[jobIdx].lastRunReturnCode == 0:
          JobsCompletingSucessfully += 1
        else:
          JobsLastExecutionFailed += 1

    if nextJobToExecute is None:
      xx = []
    else:
      xx = [nextJobToExecute]
    return{
      'TotalJobs': len(self.jobs),
      'NextJobsToExecute': xx,
      'JobsNeverRun': JobsNeverRun,
      'JobsCompletingSucessfully': JobsCompletingSucessfully,
      'JobsLastExecutionFailed': JobsLastExecutionFailed
    }
    
  def getJob(self, guid):
    try:
      r = self.jobs[str(guid)]
    except KeyError:
      raise BadRequest('Invalid Job GUID')
    return r
  def getJobByName(self, name):
    return self.jobs[str(self.jobs_name_lookup[jobClass.uniqueJobNameStatic(name)])]

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

  def updateJob(self, jobObj, newValues):
    jobClass.assertValidName(newValues['name'])
    jobClass.assertValidRepetitionInterval(newValues['repetitionInterval'], newValues['enabled'])

    oldUniqueJobName = jobObj.uniqueName()
    newUniqueJobName = jobClass.uniqueJobNameStatic(newValues['name'])
    if (str(jobObj.guid) not in self.jobs):
      raise Exception('Job to update dose not exist')
    if (oldUniqueJobName not in self.jobs_name_lookup):
      raise Exception('Old Job Name does not exist')

    # Only change the name lookup if there actually is a change
    if oldUniqueJobName != newUniqueJobName:
      if (newUniqueJobName in self.jobs_name_lookup):
        raise Exception('New Job Name already in use')
      # remove old unique name lookup
      tmpVar = self.jobs_name_lookup.pop(oldUniqueJobName)
      if tmpVar is None:
        raise Execption('Failed to remove old unique name')
      # add new unique lookup
      self.jobs_name_lookup[newUniqueJobName] = jobObj.guid

    # set recaculation of repetition interval values
    if jobObj.repetitionInterval != newValues['repetitionInterval']:
      self.nextJobToExecuteCalcRequired = True
    if jobObj.enabled != newValues['enabled']:
      self.nextJobToExecuteCalcRequired = True

    # change values in object to new values
    jobObj.setNewValues(
      self.appObj,
      newValues['name'],
      newValues['command'],
      newValues['enabled'],
      newValues['repetitionInterval'],
      newValues.get('pinned',False), 
      newValues.get('overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown',None),
      newValues.get('StateChangeSuccessJobGUID',None),
      newValues.get('StateChangeFailJobGUID',None),
      newValues.get('StateChangeUnknownJobGUID',None)
    )

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
  #  - Editing a job
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

  def registerRunDetails(self, jobGUID, newLastRunDate, newLastRunReturnCode, triggerExecutionObj):
    self.jobs[str(jobGUID)].registerRunDetails(self.appObj, newLastRunDate, newLastRunReturnCode, triggerExecutionObj)

  #funciton for testing allowing us to pretend it is currently a different time
  def recaculateExecutionTimesBasedonNewTime(self, curTime):
    for jobIdx in self.jobs:
      self.jobs[jobIdx].setNextScheduledRun(curTime)
    self.nextJobToExecuteCalcRequired = True


def resetData(appObj):
  appObj.appData['jobsData']=jobsDataClass(appObj)

def registerAPI(appObj):
  # Fields required to create a Job
  jobCreationModel = getJobCreationModel(appObj)

  nsJobs = appObj.flastRestPlusAPIObject.namespace('jobs', description='Job Operations')
  @nsJobs.route('/')
  class jobList(Resource):
    '''Operations relating to jobs'''

    @nsJobs.doc('getjobs')
    @nsJobs.marshal_with(appObj.getResultModel(getJobModel(appObj)))
    @appObj.flastRestPlusAPIObject.response(200, 'Success')
    @appObj.addStandardSortParams(nsJobs)
    def get(self):
      '''Get Jobs'''
      def outputJob(item):
        return appObj.appData['jobsData'].jobs[item]._caculatedDict(appObj)
      def filterJob(item, whereClauseText): #if multiple separated by spaces each is passed individually and anded together
        if whereClauseText.find('=') == -1:
          if appObj.appData['jobsData'].jobs[item].name.upper().find(whereClauseText) != -1:
            return True
          if appObj.appData['jobsData'].jobs[item].command.upper().find(whereClauseText) != -1:
            return True
          return False
        #only supports a single search param
        sp = whereClauseText.split("=")
        if sp[0]=="PINNED":
          if sp[1]=="TRUE":
             return appObj.appData['jobsData'].jobs[item].pinned
          if sp[1]=="FALSE":
             return not appObj.appData['jobsData'].jobs[item].pinned
          return False
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
      jobObj = jobClass(
        appObj,
        content['name'], 
        content['command'], 
        content['enabled'], 
        content['repetitionInterval'], 
        content.get('pinned',False), 
        content.get('overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown',None),
        content.get('StateChangeSuccessJobGUID',None),
        content.get('StateChangeFailJobGUID',None),
        content.get('StateChangeUnknownJobGUID',None)
      )
      res = appObj.appData['jobsData'].addJob(jobObj)
      if res['msg']!='OK':
        raise BadRequest(res['msg'])
      return appObj.appData['jobsData'].getJob(res['guid'])._caculatedDict(appObj)

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
        return appObj.appData['jobsData'].getJob(guid)._caculatedDict(appObj)
      except:
        try:
          return appObj.appData['jobsData'].getJobByName(guid)._caculatedDict(appObj)
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
      return deletedJob._caculatedDict(appObj)

    @nsJobs.doc('update_job')
    @nsJobs.expect(jobCreationModel, validate=True)
    @nsJobs.response(200, 'Job Updated')
    @nsJobs.response(400, 'Validation Error')
    @appObj.flastRestPlusAPIObject.marshal_with(getJobModel(appObj), code=200, description='Job updated')
    def put(self, guid):
      '''Update job'''
      Job = None
      try:
        Job = appObj.appData['jobsData'].getJob(guid)
      except:
        try:
          Job = appObj.appData['jobsData'].getJobByName(guid)
        except:
          raise BadRequest('Invalid Job Identifier')
      appObj.appData['jobsData'].updateJob(Job, request.get_json())
      return Job._caculatedDict(appObj)

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
      return appObj.jobExecutor.submitJobForExecution(guid, content['name'], True)._caculatedDict()

    @nsJobs.doc('getjobexecutions')
    @nsJobs.marshal_with(appObj.getResultModel(getJobExecutionModel(appObj)))
    @appObj.flastRestPlusAPIObject.response(200, 'Success')
    @appObj.addStandardSortParams(nsJobs)
    def get(self, guid):
      '''Get Job Executions'''
      jobObj = None
      try:
        jobObj = appObj.appData['jobsData'].getJob(guid)
      except:
        try:
          jobObj = appObj.appData['jobsData'].getJobByName(guid)
        except:
          raise BadRequest('Invalid Job Identifier')

      def outputJobExecution(item):
        return item._caculatedDict()
      def filterJobExecution(item, whereClauseText): #if multiple separated by spaces each is passed individually and anded together
        return True
      return appObj.getPaginatedResult(
        appObj.jobExecutor.getAllJobExecutions(jobObj.guid),
        outputJobExecution,
        request,
        filterJobExecution
      )


