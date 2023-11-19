#appObj.py - This file contains the main application object
# to be constructed by app.py

#All times will be passed to callers in UTC
# it is up to the callers to convert into any desired user timezone

import pytz

from baseapp_for_restapi_backend_with_swagger import AppObjBaseClass as parAppObj, readFromEnviroment
from serverInfoAPI import registerAPI as registerMainApi
from jobsDataAPI import registerAPI as registerJobsApi, resetData as resetJobsData, getJobServerInfoModel
from jobExecutionsDataAPI import registerAPI as registerJobExecutionsApi
import APIs
import Logic

from flask_restx import fields, Api as flaskApi
from flask import Blueprint
from JobExecutor import JobExecutorClass
import datetime
import json
from object_store_abstraction import createObjectStoreInstance
from APIClients import GoogleClient

from ExternalTriggers import ExternalTriggerManager, register_api as registerTriggerApi, register_private_api as registerTriggerPrivateApi

InvalidObjectStoreConfigInvalidJSONException = Exception('APIAPP_OBJECTSTORECONFIG value is not valid JSON')
InvalidMonitorCheckTempStateConfigInvalidJSONException = Exception('APIAPP_MONITORCHECKTEMPSTATECONFIG value is not valid JSON')

class appObjClass(parAppObj):
  jobExecutor = None
  userforjobs = None
  groupforjobs = None
  serverStartTime = None
  curDateTimeOverrideForTesting = None
  minutesBeforeMostRecentCompletionStatusBecomesUnknown = None
  objectStore = None
  monitorCheckTempState = None
  externalTriggerManager = None
  APIAPP_TRIGGERAPIURL = None
  DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE = None

  def init(self, env, serverStartTime, testingMode = False, objectStoreTestingPopulationHookFn = None):
    try:
      self.minutesBeforeMostRecentCompletionStatusBecomesUnknown = 49 * 60
      self.curDateTimeOverrideForTesting = None
      self.serverStartTime = serverStartTime
      if self.jobExecutor is not None:
        #for testing we init multiple times. We need to stop the thread running in this case
        self.jobExecutor.stopThreadRunning()
        if self.jobExecutor.is_alive():
          self.jobExecutor.join()
        self.jobExecutor = None

      self.DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE = readFromEnviroment(env, 'DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE', "notactive", None)
      # Test client on start up. Make sure credentials file is there and working
      if self.DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE == "notactive":
        print("No google client setup")
      else:
        print("Checking google client")
        GoogleClient(client_Secret_file=self.DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE)

      self.APIAPP_TRIGGERAPIURL = readFromEnviroment(env, 'APIAPP_TRIGGERAPIURL', None, None)
      DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD = readFromEnviroment(env, 'DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD', None, None)
      self.externalTriggerManager = ExternalTriggerManager(
        DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD=DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD,
        appObj=self
      )

      super(appObjClass, self).init(env, serverStartTime, testingMode, serverinfoapiprefix='')
      resetJobsData(self)

      self.userforjobs = readFromEnviroment(env, 'APIAPP_USERFORJOBS', None, None)
      self.groupforjobs = readFromEnviroment(env, 'APIAPP_GROUPFORJOBS', None, None)
      skipUserCheck = readFromEnviroment(env, 'APIAPP_SKIPUSERCHECK', False, [False, True])
      self.jobExecutor = JobExecutorClass(self, skipUserCheck)

      #When we are testing we will launch the loop iterations manually
      if not testingMode:
        self.jobExecutor.start()

      objectStoreConfigJSON = readFromEnviroment(env, 'APIAPP_OBJECTSTORECONFIG', '{}', None)
      objectStoreConfigDict = None
      try:
        if objectStoreConfigJSON != '{}':
          objectStoreConfigDict = json.loads(objectStoreConfigJSON)
      except Exception as err:
        print(err) # for the repr
        print(str(err)) # for just the message
        print(err.args) # the arguments that the exception has been called with.
        raise(InvalidObjectStoreConfigInvalidJSONException)

      fns = {
        'getCurDateTime': self.getCurDateTime
      }
      self.objectStore = createObjectStoreInstance(objectStoreConfigDict, fns)

      if testingMode:
        if objectStoreTestingPopulationHookFn is not None:
          # Give our tests the chance to inject some base data
          objectStoreTestingPopulationHookFn(objectStore = self.objectStore)

      monitorCheckTempStateConfigJSON = readFromEnviroment(env, 'APIAPP_MONITORCHECKTEMPSTATECONFIG', '{}', None)
      monitorCheckTempStateConfigDict = None
      try:
        if monitorCheckTempStateConfigJSON != '{}':
          monitorCheckTempStateConfigDict = json.loads(monitorCheckTempStateConfigJSON)
      except Exception as err:
        print(err) # for the repr
        print(str(err)) # for just the message
        print(err.args) # the arguments that the exception has been called with.
        raise(InvalidMonitorCheckTempStateConfigInvalidJSONException)

      self.monitorCheckTempState = Logic.MonitorCheckTempState(monitorCheckTempStateConfigDict, fns)

      appObj.appData['jobsData'].loadFromObjectStore()

    except Exception as a:
      self.stopThread()
      raise a


  def initOnce(self):
    super(appObjClass, self).initOnce()
    registerMainApi(self)
    registerJobsApi(self)
    registerJobExecutionsApi(self)
    APIs.registerAPIs(self)

    trigger_api_prefix='/triggerapi'

    # External Trigger APIs not served from /api, using /triggerapi instead
    triggerapi_blueprint = Blueprint('triggerapi', __name__)
    self.flastRestPlusExternalTriggerAPIObject = flaskApi(triggerapi_blueprint)
    self.flaskAppObject.register_blueprint(triggerapi_blueprint, url_prefix=trigger_api_prefix)
    registerTriggerApi(
      flaskObj=self.flastRestPlusExternalTriggerAPIObject,
      externalTriggerManager=self.externalTriggerManager
    )
    registerTriggerPrivateApi(
      flaskObj=self.flastRestPlusAPIObject,  #flastRestPlusAPIObject is the normal one everything else uses '/api'
      externalTriggerManager=self.externalTriggerManager
    )

    # print("URL MAP", self.flaskAppObject.url_map)

  def setTestingDateTime(self, val):
    self.curDateTimeOverrideForTesting = val
  def getCurDateTime(self):
    if self.curDateTimeOverrideForTesting is None:
      return datetime.datetime.now(pytz.timezone("UTC"))
    return self.curDateTimeOverrideForTesting

  def getServerInfoModel(self):
    serverInfoServerModel = appObj.flastRestPlusAPIObject.model('ServerInfoServer', {
      'DefaultUserTimezone': fields.String(default='Europe/London', description='Timezone used by client to display times. (All API''s use UTC so client must convert)'),
      'ServerDatetime': fields.DateTime(dt_format=u'iso8601', description='Current server date time'),
      'ServerStartupTime': fields.DateTime(dt_format=u'iso8601', description='Time the dockJob server started'),
      'TotalJobExecutions': fields.Integer(default='0',description='Number to jobs executed since server started'),
      'MinutesBeforeMostRecentCompletionStatusBecomesUnknown': fields.Integer(default='0',description='Default number of minutes a job has not been run before a job is considered to have Unknown status.')
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
    self.serverObj['MinutesBeforeMostRecentCompletionStatusBecomesUnknown'] = self.minutesBeforeMostRecentCompletionStatusBecomesUnknown
    return {'Server': self.serverObj, 'Jobs': self.appData['jobsData'].getJobServerInfo()}
    #return json.dumps({'Server': self.serverObj, 'Jobs': jobsObj})

  def stopThread(self):
    if self.jobExecutor is None:
      return
    if not self.jobExecutor.is_alive():
      return
    self.jobExecutor.stopThreadRunning()
    self.jobExecutor.join()

  #override exit gracefully to stop worker thread
  def exit_gracefully(self, signum, frame):
    self.stopThread()
    super(appObjClass, self).exit_gracefully(signum, frame)

  def resetData(self):
    resetJobsData(self)
    self.monitorCheckTempState.resetData()

  def getDerivedServerInfoData(self):
      return {
        "ExternalTriggers": self.externalTriggerManager.getStaticServerInfoData(),
        "APIAPP_TRIGGERAPIURL": self.APIAPP_TRIGGERAPIURL
      }


appObj = appObjClass()
