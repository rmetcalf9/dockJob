#appObj.py - This file contains the main application object
# to be constructed by app.py

#All times will be passed to callers in UTC
# it is up to the callers to convert into any desired user timezone

import pytz

from APIBackendWithSwaggerAppObj import APIBackendWithSwaggerAppObj
from serverInfoAPI import registerAPI as registerMainApi
from jobsDataAPI import registerAPI as registerJobsApi, resetData as resetJobsData
from flask_restplus import fields

class appObjClass(APIBackendWithSwaggerAppObj):
  def init(self, env):
    super(appObjClass, self).init(env)
    resetJobsData(self)

  def initOnce(self):
    super(appObjClass, self).initOnce()
    registerMainApi(self)
    registerJobsApi(self)

  def getServerInfoModel(self):
    serverInfoServerModel = appObj.flastRestPlusAPIObject.model('ServerInfoServer', {
      'DefaultUserTimezone': fields.String(default='Europe/London', description='Timezone used by client to display times. (All API''s use UTC so client must convert)'),
      'ServerDatetime': fields.DateTime(dt_format=u'iso8601', description='Current server date time')
    })
    serverInfoJobsModel = appObj.flastRestPlusAPIObject.model('ServerInfoJobs', {
      'NextExecuteJob': fields.String(default='', description='Next job scheduled for execution TODO'),
      'TotalJobs': fields.Integer(default='0',description='Total Jobs')
    })

    return appObj.flastRestPlusAPIObject.model('ServerInfo', {
      'Server': fields.Nested(serverInfoServerModel),
      'Jobs': fields.Nested(serverInfoJobsModel)
    })  

    #curDateTime must be in UTC
  def getServerInfoJSON(self, curDateTime):
    if (curDateTime.tzinfo != pytz.utc):
      raise self.NotUTCException
    self.serverObj['ServerDatetime'] = curDateTime.isoformat()
    return {'Server': self.serverObj, 'Jobs': self.appData['jobsData'].getJobServerInfo()}
    #return json.dumps({'Server': self.serverObj, 'Jobs': jobsObj})


appObj = appObjClass()

