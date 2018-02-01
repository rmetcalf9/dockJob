#appObj.py - This file contains the main application object
# to be constructed by app.py

#All times will be passed to callers in UTC
# it is up to the callers to convert into any desired user timezone


import json
import pytz

NotUTCException = Exception('Must be given UTC time')

class appObjClass():
  serverObj = {
    'ServerDatetime': '01-Jan-2018 13:46', #Real value never held here
    'DefaultUserTimezone': 'Europe/London'
  }
  jobs = []

  #curDateTime must be in UTC
  def getServerInfoJSON(self, curDateTime):
    if (curDateTime.tzinfo != pytz.utc):
      raise NotUTCException
    self.serverObj['ServerDatetime'] = str(curDateTime)
    jobsObj = {
      'TotalJobs': len(self.jobs),
      'NextExecuteJob': None
    }
    return json.dumps({'Server': self.serverObj, 'Jobs': jobsObj})


