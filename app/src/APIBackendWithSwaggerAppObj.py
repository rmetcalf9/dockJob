from GlobalParamaters import GlobalParamatersClass
from flask import Flask, Blueprint
import signal
from FlaskRestSubclass import FlaskRestSubclass
from flask_restplus import fields
from webfrontendAPI import webfrontendBP, registerAPI as registerWebFrontendAPI
import functools

#I need jobs to be stored in order so pagination works
from sortedcontainers import SortedDict

class APIBackendWithSwaggerAppObj():
  appData = {}
  # Implemented in my own init
  #def __init__(self):
  #  self.appData = {}
  pagesizemax = 200

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
  flaskAppObject = None
  flastRestPlusAPIObject = None
  globalParamObject = None

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
    registerWebFrontendAPI(self)
    self.flaskAppObject.register_blueprint(webfrontendBP, url_prefix='/frontend')

    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully) #sigterm is sent by docker stop command


  def exit_gracefully(self, signum, frame):
    print("Exit Gracefully called")
    raise self.ServerTerminationError()

  # Helper function to allow API's to return paginated data
  # When passed a list will returned a paginated result for that list
  def getPaginatedResult(self, list, outputFN, request, filterFN):
    offset = request.args.get('offset')
    if offset is None:
      offset = 0
    else:
      offset = int(offset)
    pagesize = request.args.get('pagesize')
    if pagesize is None:
      pagesize = 100
    else:
      pagesize = int(pagesize)

    # limit rows returned per request
    if pagesize > self.pagesizemax:
      pagesize = self.pagesizemax

    if request.args.get('query') is not None:
      origList = SortedDict(list)
      list = SortedDict()
      where_clauses = request.args.get('query').strip().upper().split(" ")
      def includeItem(item):
        for curClause in where_clauses:
          if not filterFN(item, curClause):
            return False
        return True
      for cur in origList:
        if includeItem(origList[cur]):
          list[cur]=origList[cur]

    # we now have "list" which is a filtered down list of things we need to return
    #construct a list of keys to the object, all null
    sortedKeys = []
    for cur in list:
      sortedKeys.append(cur)

    #Sort sortedKeys
    if request.args.get('sort') is not None:
      def getSortTuple(key):
        #sort keys are case sensitive
        kk = key.split(":")
        if len(kk)==0:
          raise Exception('Invalid sort key')
        elif len(kk)==1:
          return {'name': kk[0], 'desc': False}
        elif len(kk)==2:
          if kk[1].lower() == 'desc':
            return {'name': kk[0], 'desc': True}
          elif kk[1].lower() == 'asc':
            return {'name': kk[0], 'desc': False}
        raise Exception('Invalid sort key - ' + key)

      def genSortKeyGenFn(listBeingSorted, sortkey):
        def sortKeyGenFn(ite):
          try:
            # print(sortkey)
            # print(outputFN(listBeingSorted[ite])[sortkey])
            return outputFN(listBeingSorted[ite])[sortkey]
          except KeyError:
            raise Exception('Sort key ' + sortkey + ' not found')
        return sortKeyGenFn

      # sort by every sort key one at a time starting with the least significant
      for curSortKey in request.args.get('sort').split(",")[::-1]:
        sk = getSortTuple(curSortKey)
        sortedKeys.sort(key=genSortKeyGenFn(list, sk['name']), reverse=sk['desc'])

    output = []
    for cur in range(offset, (pagesize + offset)):
      if (cur<len(list)):
        output.append(outputFN(list[sortedKeys[cur]]))
        #output.append(outputFN(list[list.keys()[sortedKeys[cur]]]))

    return {
      'pagination': {
        'offset': offset,
        'pagesize': pagesize,
        'total': len(list)
      },
      'result': output
    }
  # return the model of paginated results for flask restplus
  def getResultModel(self, recordModel):
    paginationModel = self.flastRestPlusAPIObject.model('paginationList', {
      'offset': fields.Integer(default='0',description='Number to start from'),
      'pagesize': fields.Integer(default='',description='Results per page'),
      'total': fields.Integer(default='0',description='Total number of records in output')
    })
    return self.flastRestPlusAPIObject.model('resultList', {
      'pagination': fields.Nested(paginationModel),
      'result': fields.List(fields.Nested(recordModel)),
    })

  # decorator to add the standard sort params
  def addStandardSortParams(self, namespace):
    def addStandardSortParamsDec(funct):
      @functools.wraps(funct)
      @namespace.param('offset', 'Number to start from')
      @namespace.param('pagesize', 'Results per page')
      @namespace.param('query', 'Search Filter')
      @namespace.param('sort', 'Comma seperated list of sort keys. (Postfixed with :desc or :asc if required)')
      def _(*args, **kwargs):
          return funct(*args, **kwargs)
      return _
    return addStandardSortParamsDec

