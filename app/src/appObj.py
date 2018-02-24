#appObj.py - This file contains the main application object
# to be constructed by app.py

#All times will be passed to callers in UTC
# it is up to the callers to convert into any desired user timezone


import json
import pytz
from GlobalParamaters import GlobalParamatersClass
from flask import Flask
import signal
from FlaskRestSubclass import FlaskRestSubclass


NotUTCException = Exception('Must be given UTC time')

#Code required to ensure that container will exit when a signal is received
class ServerTerminationError(Exception):
  def __init__(self):
    pass
  def __str__(self):
    return "Server Terminate Error"



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

  def setFlaskAppObject(self,app):
    self.flaskAppObject = app

  def setFlastRestPlusAPIObject(self,api):
    self.flastRestPlusAPIObject = api

  # called by app.py to run the application
  def run(self, envirom):
    print(self.globalParamObject.getStartupOutput())
    self.flastRestPlusAPIObject.version = GlobalParamaters.get().version

    #appObj.flaskAppObject.config['SERVER_NAME'] = 'servername:123'
    try:
      self.flaskAppObject.run(host='0.0.0.0', port=80, debug=False)
    except ServerTerminationError as e:
      print("Stopped")

  def init(self, envirom):
    self.globalParamObject = GlobalParamatersClass(envirom)
    appObj.setFlaskAppObject(Flask(__name__))

    #Development code required to add CORS allowance in developer mode
    @self.flaskAppObject.after_request
    def after_request(response):
      if (GlobalParamaters.get().getDeveloperMode()):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
      return response

    self.setFlastRestPlusAPIObject(
      FlaskRestSubclass(appObj.flaskAppObject, 
        version='UNSET', 
        title='DocJob Scheduling Server API',
        description='API for the DockJob scheduling server', 
        doc='/apidocs/',
        default_mediatype='application/json'
      )
    )

  def exit_gracefully(self, signum, frame):
    print("Exit Gracefully called")
    raise ServerTerminationError()


appObj = appObjClass()
signal.signal(signal.SIGINT, appObj.exit_gracefully)
signal.signal(signal.SIGTERM, appObj.exit_gracefully) #sigterm is sent by docker stop command

