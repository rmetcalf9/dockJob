from flask import Flask, Blueprint, request
from appObj import appObj
from flask_restplus import Resource, fields, apidoc, reqparse
from FlaskRestSubclass import FlaskRestSubclass
import datetime
import pytz

from webfrontendAPI import webfrontendBP

t = 't'

appObj.setFlastRestPlusAPIObject(
  FlaskRestSubclass(appObj.flaskAppObject, 
    version='UNSET', 
    title='DocJob Scheduling Server API',
    description='API for the DockJob scheduling server', 
    doc='/apidocs/',
    default_mediatype='application/json'
  )
)


'''
app=None, version='1.0', title=None, description=None,
            terms_url=None, license=None, license_url=None,
            contact=None, contact_url=None, contact_email=None,
            authorizations=None, security=None, doc='/', default_id=default_id,
            default='default', default_label='Default namespace', validate=None,
            tags=None, prefix='',
            default_mediatype='application/json', decorators=None,
            catch_all_404s=False, serve_challenge_on_401=False, format_checker=None
'''

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

