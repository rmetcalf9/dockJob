from appObj import appObj
from flask_restplus import Resource, fields, apidoc


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
    'guid': fields.String(default='',description='Unique identifier for this job'),
    'creationDate': fields.String(default='',description='Unique identifier for this job'),
    'lastUpdateDate': fields.String(default='',description='Unique identifier for this job'),
    'lastRunDate': fields.String(default='',description='Unique identifier for this job'),
    # TODO Add runs to this model
})

class jobsDataClass():
  def createJob(self, request):
    a = {
      'name': 'string',
      'name2': 'aa',
      'name3': 'string'
    }
    return a

jobsData = jobsDataClass()
