#appObj.py - This file contains the main application object
# to be constructed by app.py

#All times will be passed to callers in UTC
# it is up to the callers to convert into any desired user timezone


import json
import pytz
from GlobalParamaters import GlobalParamaters


NotUTCException = Exception('Must be given UTC time')

class appObjClass():
  serverObj = {
    'ServerDatetime': '01-Jan-2018 13:46', #Real value never held here
    'DefaultUserTimezone': 'Europe/London'
  }
  jobs = []
  flaskAppObject = None
  flastRestPlusAPIObject = None
  globalParamObject = None

  #curDateTime must be in UTC
  def getServerInfoJSON(self, curDateTime):
    if (curDateTime.tzinfo != pytz.utc):
      raise NotUTCException
    self.serverObj['ServerDatetime'] = str(curDateTime)
    jobsObj = {
      'TotalJobs': len(self.jobs),
      'NextExecuteJob': None
    }
    return {'Server': self.serverObj, 'Jobs': jobsObj}
    #return json.dumps({'Server': self.serverObj, 'Jobs': jobsObj})

  def setFlaskAppOgject(self,app):
    self.flaskAppObject = app

  def setFlastRestPlusAPIObject(self,api):
    self.flastRestPlusAPIObject = api

  # called by app.py to run the application
  def run(self):
    print(GlobalParamaters.get().getStartupOutput())
    self.flastRestPlusAPIObject.version = GlobalParamaters.get().version

    #appObj.flaskAppObject.config['SERVER_NAME'] = 'servername:123'
    self.flaskAppObject.run(host='0.0.0.0', port=80, debug=False)


