from flask import request
from flask_restx import Resource, fields, apidoc
from werkzeug.exceptions import BadRequest
import uuid
import json
import datetime
import pytz
from JobExecution import getJobExecutionCreationModel, getJobExecutionModel
import enum
from jobObj import jobClass
from jobsDataObj import jobsDataClass
from APIModels import getJobModel

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
    'AfterSuccessJobGUID': fields.String(default=None,description='GUID of job to call when this completes and is still in the success state'),
    'AfterFailJobGUID': fields.String(default=None,description='GUID of job to call when this completes and is still in the fail state'),
    'AfterUnknownJobGUID': fields.String(default=None,description='GUID of job to call when this completes and is still in the unknown state'),
  })

def getJobServerInfoModel(appObj):
  return appObj.flastRestPlusAPIObject.model('ServerInfoJobs', {
    'TotalJobs': fields.Integer(default='0',description='Total Jobs'),
    'NextJobsToExecute': fields.List(fields.Nested(getJobModel(appObj.flastRestPlusAPIObject))),
    'JobsNeverRun': fields.Integer(default='-1',description='Jobs Never Run'),
    'JobsCompletingSucessfully': fields.Integer(default='-1',description='Jobs Completing Sucessfully'),
    'JobsLastExecutionFailed': fields.Integer(default='-1',description='Jobs where last execution failed')
  })

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
    @nsJobs.marshal_with(appObj.getResultModel(getJobModel(appObj.flastRestPlusAPIObject)))
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
    @appObj.flastRestPlusAPIObject.marshal_with(getJobModel(appObj.flastRestPlusAPIObject), code=200, description='Job created')
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
        content.get('StateChangeUnknownJobGUID',None),
        content.get('AfterSuccessJobGUID', None),
        content.get('AfterFailJobGUID', None),
        content.get('AfterUnknownJobGUID', None),
        guid=None,
        verifyDependentJobGuids=True,
        loadingObjectVersion=None,
        PrivateExternalTrigger={"triggerActive": False}
      )

      storeConnection = appObj.objectStore._getConnectionContext()
      def someFn(connectionContext):
        return appObj.appData['jobsData'].addJob(jobObj, connectionContext)
      res = storeConnection.executeInsideTransaction(someFn)

      if res['msg']!='OK':
        raise BadRequest(res['msg'])
      return appObj.appData['jobsData'].getJob(res['guid'])._caculatedDict(appObj)

  @nsJobs.route('/<string:guid>')
  @nsJobs.response(400, 'Job not found')
  @nsJobs.param('guid', 'Job identifier (or name)')
  class job(Resource):
    '''Show a single Job'''
    @nsJobs.doc('get_job')
    @nsJobs.marshal_with(getJobModel(appObj.flastRestPlusAPIObject))
    def get(self, guid):
      '''Fetch a given resource'''
      try:
        return appObj.appData['jobsData'].getJob(guid)._caculatedDict(appObj)
      except:
        try:
          return appObj.appData['jobsData'].getJobByName(guid)._caculatedDict(appObj)
        except Exception as e:
          raise BadRequest("Failed to find job with guid or name matching " + guid)
          #raise BadRequest(type(e).__name__ + " - " + str(e.args))
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

      storeConnection = appObj.objectStore._getConnectionContext()
      def someFn(connectionContext):
        appObj.appData['jobsData'].deleteJob(deletedJob, connectionContext)
      storeConnection.executeInsideTransaction(someFn)

      return deletedJob._caculatedDict(appObj)

    @nsJobs.doc('update_job')
    @nsJobs.expect(jobCreationModel, validate=True)
    @nsJobs.response(200, 'Job Updated')
    @nsJobs.response(400, 'Validation Error')
    @appObj.flastRestPlusAPIObject.marshal_with(getJobModel(appObj.flastRestPlusAPIObject), code=200, description='Job updated')
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

      storeConnection = appObj.objectStore._getConnectionContext()
      def someFn(connectionContext):
        appObj.appData['jobsData'].updateJob(Job, request.get_json(), connectionContext)
      storeConnection.executeInsideTransaction(someFn)

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
      stdinData = None
      if "stdinData" in content:
        stdinData = content["stdinData"].encode("utf-8")
      return appObj.jobExecutor.submitJobForExecution(guid, content['name'], True, stdinData=stdinData)._caculatedDict()

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


