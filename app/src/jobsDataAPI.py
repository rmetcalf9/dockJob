from flask import request
from flask_restplus import Resource, fields, apidoc
from werkzeug.exceptions import BadRequest
import uuid
import json
import datetime
# from pytz import timezone
import pytz
from RepetitionInterval import RepetitionIntervalClass

class jobsDataClass():
  # map of guid to Job
  jobs = {}
  # map of Job name to guid
  jobs_name_lookup = {}
  def __init__(self):
    self.jobs = {}
    self.jobs_name_lookup = {}
    pass

  def getJob(self, guid):
    return self.jobs[str(guid)]

  def nameUniqunessFn(self, name):
    return name.strip().upper()
    
  # return GUID or error
  def addJob(self, job):
    uniqueJobName = self.nameUniqunessFn(job['name'])
    if (str(job['guid']) in self.jobs):
      return {'msg': 'GUID already in use', 'guid':''}
    if (uniqueJobName in self.jobs_name_lookup):
      return {'msg': 'Job Name already in use', 'guid':''}
    if (job['repetitionInterval'] != None):
      if (job['repetitionInterval'] != ''):
        try:
          ri = RepetitionIntervalClass(job['repetitionInterval'])
        except:
          return {'msg': 'Invalid Repetition Interval', 'guid':''}
        job['nextScheduledRun'] = ri.getNextOccuranceDatetime(datetime.datetime.now(pytz.timezone("UTC")))
    self.jobs[str(job['guid'])] = job
    self.jobs_name_lookup[uniqueJobName] = uniqueJobName
    return {'msg': 'OK', 'guid':job['guid']}

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
  class jobs(Resource):
    '''Operations relating to jobs'''

    @nsJobs.doc('getjobs')
    # @ns.marshal_list_with(todo)
    def get(self):
      '''Get Jobs'''
      return []

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
        'guid': uuid.uuid4(),
        'name': content['name'],
        'command': content['command'],
        'enabled': content['enabled'],
        'repetitionInterval': content['repetitionInterval'],
        'creationDate': curTime.isoformat(),
        'lastUpdateDate': curTime.isoformat()
      }
      res = appObj.appData['jobsData'].addJob(newJob)
      if res['msg']!='OK':
        raise BadRequest(res['msg'])
      return appObj.appData['jobsData'].getJob(res['guid'])

