#appObj.py - This file contains the main application object
# to be constructed by app.py

#All times will be passed to callers in UTC
# it is up to the callers to convert into any desired user timezone

import pytz

from APIBackendWithSwaggerAppObj import APIBackendWithSwaggerAppObj
from serverInfoAPI import registerAPI as registerMainApi
from jobsDataAPI import registerAPI as registerJobsApi, resetData as resetJobsData

class appObjClass(APIBackendWithSwaggerAppObj):
  def init(self, env):
    super(appObjClass, self).init(env)
    resetJobsData(self)

  def initOnce(self):
    super(appObjClass, self).initOnce()
    registerMainApi(self)
    registerJobsApi(self)

  #curDateTime must be in UTC
  def getServerInfoJSON(self, curDateTime):
    if (curDateTime.tzinfo != pytz.utc):
      raise self.NotUTCException
    self.serverObj['ServerDatetime'] = str(curDateTime)
    return {'Server': self.serverObj, 'Jobs': self.appData['jobsData'].getJobServerInfo()}
    #return json.dumps({'Server': self.serverObj, 'Jobs': jobsObj})


appObj = appObjClass()

