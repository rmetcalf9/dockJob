import pytz
from GlobalParamaters import GlobalParamatersClass
from flask import Flask, Blueprint
import signal
from FlaskRestSubclass import FlaskRestSubclass
from webfrontendAPI import webfrontendBP


class APIBackendWithSwaggerAppObj():
  appData = {}
  # Implemented in my own init
  #def __init__(self):
  #  self.appData = {}

  NotUTCException = Exception('Must be given UTC time')
  class ServerTerminationError(Exception):
    def __init__(self):
      pass
    def __str__(self):
      return "Server Terminate Error"

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
      raise self.NotUTCException
    self.serverObj['ServerDatetime'] = str(curDateTime)
    jobsObj = {
      'TotalJobs': len(self.jobs),
      'NextExecuteJob': None
    }
    return {'Server': self.serverObj, 'Jobs': jobsObj}
    #return json.dumps({'Server': self.serverObj, 'Jobs': jobsObj})

  # called by app.py to run the application
  def run(self):
    if (self.isInitOnce == False):
      raise Exception('Trying to run app without initing')
    print(self.globalParamObject.getStartupOutput())
    self.flastRestPlusAPIObject.version = self.globalParamObject.version

    #appObj.flaskAppObject.config['SERVER_NAME'] = 'servername:123'
    try:
      self.flaskAppObject.run(host='0.0.0.0', port=80, debug=False)
    except self.ServerTerminationError as e:
      print("Stopped")

  isInitOnce = False
  def init(self, envirom):
    self.appData = {}
    self.globalParamObject = GlobalParamatersClass(envirom)
    if (self.isInitOnce):
      return
    self.isInitOnce = True
    self.initOnce()

  def initOnce(self):
    self.flaskAppObject = Flask(__name__)

    #Development code required to add CORS allowance in developer mode
    @self.flaskAppObject.after_request
    def after_request(response):
      if (self.globalParamObject.getDeveloperMode()):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
      return response

    self.flastRestPlusAPIObject = FlaskRestSubclass(self.flaskAppObject, 
      version='UNSET', 
      title='DocJob Scheduling Server API',
      description='API for the DockJob scheduling server', 
      doc='/apidocs/',
      default_mediatype='application/json'
    )
    self.flastRestPlusAPIObject.setExtraParams(
      self.globalParamObject.apidocsurl, 
      self.globalParamObject.getAPIDOCSPath(), 
      self.globalParamObject.overrideAPIDOCSPath, 
      self.globalParamObject.getAPIPath()
    )

    api_blueprint = Blueprint('api', __name__)
    self.flastRestPlusAPIObject.init_app(api_blueprint)  

    self.flaskAppObject.register_blueprint(api_blueprint, url_prefix='/api')
    self.flaskAppObject.register_blueprint(webfrontendBP, url_prefix='/frontend')

    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully) #sigterm is sent by docker stop command


  def exit_gracefully(self, signum, frame):
    print("Exit Gracefully called")
    raise self.ServerTerminationError()

  # Helper function to allow API's to return paginated data
  # When passed a list will returned a paginated result for that list
  def getPaginatedResult(self, list, outputFN, request):
    offset = request.args.get('offset')
    if offset is None:
      offset = 0
    else:
      offset = int(offset)
    pagesize = request.args.get('pagesize')
    if pagesize is None:
      pagesize = 20
    else:
      pagesize = int(pagesize)
    output = []
    for cur in range(offset, (pagesize + offset)):
      if (cur<len(list)):
        output.append(outputFN(list[list.keys()[cur]]))
    return {
      'pagination': {
        'offset': offset,
        'pagesize': pagesize,
        'total': len(list)
      },
      'result': output
    }
