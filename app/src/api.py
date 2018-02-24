from flask import Flask, Blueprint, request
from appObj import appObj
from flask_restplus import Resource, fields, apidoc, reqparse
import datetime
import pytz

from webfrontendAPI import webfrontendBP

t = 't'

def registerAPI(appObj):

  api_blueprint = Blueprint('api', __name__)
  appObj.flastRestPlusAPIObject.init_app(api_blueprint)  

  appObj.flaskAppObject.register_blueprint(api_blueprint, url_prefix='/api')

  nsServerinfo = appObj.flastRestPlusAPIObject.namespace('serverinfo', description='General Server Operations')
  @nsServerinfo.route('/')
  class servceInfo(Resource):
    '''General Server Operations XXXXX'''
    @nsServerinfo.doc('getserverinfo')
    # @ns.marshal_list_with(todo)
    def get(self):
      '''Get general information about the dockjob server'''
      curDatetime = datetime.datetime.now(pytz.utc)
      return appObj.getServerInfoJSON(curDatetime)

  from jobsData import t

  appObj.flaskAppObject.register_blueprint(webfrontendBP, url_prefix='/frontend')

