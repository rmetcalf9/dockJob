from .monitorCheckTempState import registerAPI as monitorCheckTemp_registerAPI

def registerAPIs(appObj):
  nsMonitorCheckTemp = appObj.flastRestPlusAPIObject.namespace('monitorCheckTempState', description='Monitor Check Temp State API')

  monitorCheckTemp_registerAPI(appObj=appObj, APInamespace=nsMonitorCheckTemp)
