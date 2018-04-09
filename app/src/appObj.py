#appObj.py - This file contains the main application object
# to be constructed by app.py

#All times will be passed to callers in UTC
# it is up to the callers to convert into any desired user timezone

import pytz

from baseapp_for_restapi_backend_with_swagger import appObj
from serverInfoAPI import registerAPI as registerMainApi
from jobsDataAPI import registerAPI as registerJobsApi, resetData as resetJobsData, getJobServerInfoModel
from jobExecutionsDataAPI import registerAPI as registerJobExecutionsApi
from flask_restplus import fields
from JobExecutor import JobExecutorClass
import time

MissingUserForJobsException = Exception('Missing user for Jobs (set APIAPP_USERFORJOBS)')
MissingGroupForJobsException = Exception('Missing group for Jobs (set APIAPP_GROUPFORJOBS)')

class appObjClass(appObj):
  jobExecutor = None
  userforjobs = None
  groupforjobs = None
  serverStartTime = None

  def init(self, env, serverStartTime, testingMode = False):
    self.serverStartTime = serverStartTime
    if self.jobExecutor is not None:
      #for testing we init multiple times. We need to stop the thread running in this case
      self.jobExecutor.stopThreadRunning()
      if self.jobExecutor.isAlive():
        self.jobExecutor.join()
      self.jobExecutor = None
    super(appObjClass, self).init(env)
    resetJobsData(self)
    self.userforjobs = self.globalParamObject.readFromEnviroment(env, 'APIAPP_USERFORJOBS', None, MissingUserForJobsException, None)
    self.groupforjobs = self.globalParamObject.readFromEnviroment(env, 'APIAPP_GROUPFORJOBS', None, MissingGroupForJobsException, None)
    skipUserCheck = self.globalParamObject.readFromEnviroment(env, 'APIAPP_SKIPUSERCHECK', False, MissingGroupForJobsException, None)
    self.jobExecutor = JobExecutorClass(self, skipUserCheck)

    #When we are testing we will launch the loop iterations manually
    if not testingMode:
      self.jobExecutor.start()

  def initOnce(self):
    super(appObjClass, self).initOnce()
    registerMainApi(self)
    registerJobsApi(self)
    registerJobExecutionsApi(self)

  def getServerInfoModel(self):
    serverInfoServerModel = appObj.flastRestPlusAPIObject.model('ServerInfoServer', {
      'DefaultUserTimezone': fields.String(default='Europe/London', description='Timezone used by client to display times. (All API''s use UTC so client must convert)'),
      'ServerDatetime': fields.DateTime(dt_format=u'iso8601', description='Current server date time'),
      'ServerStartupTime': fields.DateTime(dt_format=u'iso8601', description='Time the dockJob server started'),
      'TotalJobExecutions': fields.Integer(default='0',description='Number to jobs executed since server started')
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
    self.serverObj['ServerStartupTime'] = self.serverStartTime.isoformat()
    self.serverObj['TotalJobExecutions'] = self.jobExecutor.totalExecutions
    return {'Server': self.serverObj, 'Jobs': self.appData['jobsData'].getJobServerInfo()}
    #return json.dumps({'Server': self.serverObj, 'Jobs': jobsObj})

  def stopThread(self):
    if self.jobExecutor is None:
      return
    if not self.jobExecutor.isAlive():
      return
    self.jobExecutor.stopThreadRunning()
    self.jobExecutor.join()

  #override exit gracefully to stop worker thread
  def exit_gracefully(self, signum, frame):
    self.stopThread()
    super(appObjClass, self).exit_gracefully(signum, frame)

appObj = appObjClass()

