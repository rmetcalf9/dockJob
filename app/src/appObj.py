#appObj.py - This file contains the main application object
# to be constructed by app.py

#All times will be passed to callers in UTC
# it is up to the callers to convert into any desired user timezone


from APIBackendWithSwaggerAppObj import APIBackendWithSwaggerAppObj
from api import registerAPI as registerMainApi
from jobsData import registerAPI as registerJobsApi

class appObjClass(APIBackendWithSwaggerAppObj):
  def initOnce(self):
    super(appObjClass, self).initOnce()
    registerMainApi(self)
    registerJobsApi(self)


appObj = appObjClass()

