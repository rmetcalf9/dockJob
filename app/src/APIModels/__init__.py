from flask_restx import fields


def getExternalTriggerJobModel(flastRestPlusAPIObject):
    return flastRestPlusAPIObject.model('triggerActive', {
        'triggerActive': fields.Boolean(default=False, description='Is auto triggeing enabled'),
    })


def getJobModel(flastRestPlusAPIObject):
  return flastRestPlusAPIObject.model('Job', {
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
      'AfterSuccessJobGUID': fields.String(default=None,description='GUID of job to call when this completes and is still in the success state'),
      'AfterFailJobGUID': fields.String(default=None,description='GUID of job to call when this completes and is still in the fail state'),
      'AfterUnknownJobGUID': fields.String(default=None,description='GUID of job to call when this completes and is still in the unknown state'),
      'StateChangeSuccessJobNAME': fields.String(default=None,description='READONLY - Name of job to call when this jobs state changes to Success'),
      'StateChangeFailJobNAME': fields.String(default=None,description='READONLY - Name of job to call when this jobs state changes to Fail'),
      'StateChangeUnknownJobNAME': fields.String(default=None,description='READONLY - Name of job to call when this jobs state changes to Unknown'),
      'AfterSuccessJobNAME': fields.String(default=None,description='READONLY - Name of job to call when this completes and is still in the success state'),
      'AfterFailJobNAME': fields.String(default=None,description='READONLY - Name of job to call when this completes and is still in the fail state'),
      'AfterUnknownJobNAME': fields.String(default=None,description='READONLY - Name of job to call when this completes and is still in the unknown state'),
      'ExternalTrigger': fields.Nested(getExternalTriggerJobModel(flastRestPlusAPIObject)),
    })
  return jobModel

def getErrorModel(flastRestPlusAPIObject):
    return flastRestPlusAPIObject.model('ErrorResponse', {
        'result': fields.String(default=''),
        'message': fields.String(default='')
    })