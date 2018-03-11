#appObj.py - This file contains the main application object
# to be constructed by app.py

#All times will be passed to callers in UTC
# it is up to the callers to convert into any desired user timezone

import pytz

from APIBackendWithSwaggerAppObj import APIBackendWithSwaggerAppObj
from serverInfoAPI import registerAPI as registerMainApi
from jobsDataAPI import registerAPI as registerJobsApi, resetData as resetJobsData, getJobServerInfoModel
from flask_restplus import fields
from JobExecutor import JobExecutorClass
import time

MissingUserForJobsException = Exception('Missing user for Jobs (set APIAPP_USERFORJOBS)')
MissingGroupForJobsException = Exception('Missing group for Jobs (set APIAPP_GROUPFORJOBS)')

class appObjClass(APIBackendWithSwaggerAppObj):
  jobExecutor = None
  userforjobs = None
  groupforjobs = None

  def init(self, env):
    super(appObjClass, self).init(env)
    resetJobsData(self)
    self.userforjobs = self.globalParamObject.readFromEnviroment(env, 'APIAPP_USERFORJOBS', None, MissingUserForJobsException, None)
    self.groupforjobs = self.globalParamObject.readFromEnviroment(env, 'APIAPP_GROUPFORJOBS', None, MissingGroupForJobsException, None)
    skipUserCheck = self.globalParamObject.readFromEnviroment(env, 'APIAPP_SKIPUSERCHECK', False, MissingGroupForJobsException, None)
    self.jobExecutor = JobExecutorClass(self, skipUserCheck)
    self.jobExecutor.start()

  def initOnce(self):
    super(appObjClass, self).initOnce()
    registerMainApi(self)
    registerJobsApi(self)

  def getServerInfoModel(self):
    serverInfoServerModel = appObj.flastRestPlusAPIObject.model('ServerInfoServer', {
      'DefaultUserTimezone': fields.String(default='Europe/London', description='Timezone used by client to display times. (All API''s use UTC so client must convert)'),
      'ServerDatetime': fields.DateTime(dt_format=u'iso8601', description='Current server date time')
    })

    return appObj.flastRestPlusAPIObject.model('ServerInfo', {
      'Server': fields.Nested(serverInfoServerModel),
      'Jobs': fields.Nested(getJobServerInfoModel(appObj))
    })  

    #curDateTime must be in UTC
  def getServerInfoJSON(self, curDateTime):
    if (curDateTime.tzinfo != pytz.utc):
      raise self.NotUTCException
    self.serverObj['ServerDatetime'] = curDateTime.isoformat()
    return {'Server': self.serverObj, 'Jobs': self.appData['jobsData'].getJobServerInfo()}
    #return json.dumps({'Server': self.serverObj, 'Jobs': jobsObj})

  #override exit gracefully to stop worker thread
  def exit_gracefully(self, signum, frame):
    self.jobExecutor.stopThreadRunning()
    time.sleep(0.3) #give thread a chance to stop
    super(appObjClass, self).exit_gracefully(signum, frame)

appObj = appObjClass()

