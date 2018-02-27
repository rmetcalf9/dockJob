from flask import request
from flask_restplus import Resource, fields, apidoc
from werkzeug.exceptions import BadRequest
import uuid
import json
import datetime
# from pytz import timezone
import pytz
from RepetitionInterval import RepetitionIntervalClass

#I need jobs to be stored in order so pagination works
from sortedcontainers import SortedDict

class jobsDataClass():
  # map of guid to Job
  jobs = None
  # map of Job name to guid
  jobs_name_lookup = None
  def __init__(self):
    self.jobs = SortedDict()
    self.jobs_name_lookup = SortedDict()
    pass

  def getJob(self, guid):
    return self.jobs[str(guid)]
  def getJobByName(self, name):
    return self.jobs[str(self.jobs_name_lookup[self.nameUniqunessFn(name)])]

  def nameUniqunessFn(self, name):
    return name.strip().upper()
    
  # return GUID or error
  def addJob(self, job):
    if (len(job['name'])<2):
      return {'msg': 'Job name must be more than 2 characters', 'guid':''}
    uniqueJobName = self.nameUniqunessFn(job['name'])
    if (str(job['guid']) in self.jobs):
      return {'msg': 'GUID already in use', 'guid':''}
    if (uniqueJobName in self.jobs_name_lookup):
      return {'msg': 'Job Name already in use - ' + uniqueJobName, 'guid':''}
    if (job['repetitionInterval'] != None):
      if (job['repetitionInterval'] != ''):
        try:
          ri = RepetitionIntervalClass(job['repetitionInterval'])
        except:
          return {'msg': 'Invalid Repetition Interval', 'guid':''}
        job['nextScheduledRun'] = ri.getNextOccuranceDatetime(datetime.datetime.now(pytz.timezone("UTC"))).isoformat()
    self.jobs[str(job['guid'])] = job
    self.jobs_name_lookup[uniqueJobName] = job['guid']
    return {'msg': 'OK', 'guid':job['guid']}

  def deleteJob(self, jobObj):
    uniqueJobName = self.nameUniqunessFn(jobObj['name'])
    self.jobs_name_lookup.pop(uniqueJobName)
    self.jobs.pop(jobObj['guid'])

def resetData(appObj):
  appObj.appData['jobsData']=jobsDataClass()

def registerAPI(appObj):
  # Fields required to create a Job
  jobCreationModel = appObj.flastRestPlusAPIObject.model('JobCreation', {
    'name': fields.String(default=''),
    'command': fields.String(default=''),
    'enabled': fields.Boolean(default=False,description='Is the job currently enabled'),
    'repetitionInterval': fields.String(default='',description='How the job is scheduled to run'),
  })

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
    # TODO Add runs to this model
  })

  nsJobs = appObj.flastRestPlusAPIObject.namespace('jobs', description='Job Operations')
  @nsJobs.route('/')
  class jobList(Resource):
    '''Operations relating to jobs'''

    @nsJobs.doc('getjobs')
    @nsJobs.marshal_with(appObj.getResultModel(jobModel))
    @appObj.flastRestPlusAPIObject.response(200, 'Success')
    @nsJobs.param('offset', 'Number to start from')
    @nsJobs.param('pagesize', 'Results per page')
    @nsJobs.param('query', 'Search Filter')
    def get(self):
      '''Get Jobs'''
      def outputJob(item):
        return appObj.appData['jobsData'].jobs[item]
      def filterJob(item, whereClauseText): #if mutiple seperated by spaces each is passed individually and anded together
        if appObj.appData['jobsData'].jobs[item]['name'].upper().find(whereClauseText) != -1:
          return True
        if appObj.appData['jobsData'].jobs[item]['command'].upper().find(whereClauseText) != -1:
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
    @appObj.flastRestPlusAPIObject.marshal_with(jobModel, code=200, description='Job created')
    def post(self):
      '''Create Job'''
      content = request.get_json()
      curTime = datetime.datetime.now(pytz.timezone("UTC"))
      newJob = {
        'guid': str(uuid.uuid4()),
        'name': content['name'],
        'command': content['command'],
        'enabled': content['enabled'],
        'repetitionInterval': content['repetitionInterval'],
        'creationDate': curTime.isoformat(),
        'lastUpdateDate': curTime.isoformat(),
        'lastRunDate': None
      }
      res = appObj.appData['jobsData'].addJob(newJob)
      if res['msg']!='OK':
        raise BadRequest(res['msg'])
      return appObj.appData['jobsData'].getJob(res['guid'])

  @nsJobs.route('/<string:guid>')
  @nsJobs.response(400, 'Job not found')
  @nsJobs.param('guid', 'Job identifier (or name)')
  class job(Resource):
    '''Show a single Job'''
    @nsJobs.doc('get_job')
    @nsJobs.marshal_with(jobModel)
    def get(self, guid):
      '''Fetch a given resource'''
      try:
        return appObj.appData['jobsData'].getJob(guid)
      except:
        try:
          return appObj.appData['jobsData'].getJobByName(guid)
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
      return deletedJob
