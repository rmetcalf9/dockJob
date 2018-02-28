from flask_restplus import Resource
import datetime
import pytz

def registerAPI(appObj):
  nsServerinfo = appObj.flastRestPlusAPIObject.namespace('serverinfo', description='General Server Operations')
  @nsServerinfo.route('/')
  class servceInfo(Resource):
    '''General Server Operations XXXXX'''
    @nsServerinfo.doc('getserverinfo')
    @nsServerinfo.marshal_with(appObj.getServerInfoModel())
    @nsServerinfo.response(200, 'Success')
    def get(self):
     '''Get general information about the dockjob server'''
     curDatetime = datetime.datetime.now(pytz.utc)
     return appObj.getServerInfoJSON(curDatetime)


