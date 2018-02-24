from flask_restplus import Resource, fields, apidoc, reqparse
import datetime
import pytz

def registerAPI(appObj):

  nsServerinfo = appObj.flastRestPlusAPIObject.namespace('serverinfo', description='General Server Operations')
  @nsServerinfo.route('/')
  class servceInfo(Resource):
    '''General Server Operations XXXXX'''
    @nsServerinfo.doc('getserverinfo')
    def get(self):
     '''Get general information about the dockjob server'''
     curDatetime = datetime.datetime.now(pytz.utc)
     return appObj.getServerInfoJSON(curDatetime)


