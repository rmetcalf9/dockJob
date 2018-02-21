from flask import Flask, Blueprint, request
from appObj import appObjClass
from flask_restplus import Resource, fields, apidoc, reqparse
from FlaskRestSubclass import FlaskRestSubclass
import datetime
import pytz

appObj = appObjClass()
appObj.setFlaskAppOgject(Flask(__name__))

from webfrontendAPI import webfrontendBP

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
  '''Genaral Server Opeations XXXXX'''
  @nsServerinfo.doc('getserverinfo')
  # @ns.marshal_list_with(todo)
  def get(self):
    '''Get general information about the dockjob server'''
    curDatetime = datetime.datetime.now(pytz.utc)
    return appObj.getServerInfoJSON(curDatetime)

jobModel = appObj.flastRestPlusAPIObject.model('Job', {
    'name': fields.String,
    'name2': fields.String(),
    'name3': fields.String()
})

nsJobs = appObj.flastRestPlusAPIObject.namespace('jobs', description='Job Operations')
@nsJobs.route('/')
class servceInfo(Resource):
  '''Operations relating to jobs'''

  @nsJobs.doc('getjobs')
  # @ns.marshal_list_with(todo)
  def get(self):
    '''Get Jobs'''
    return []

  @nsJobs.doc('putjobs')
  @appObj.flastRestPlusAPIObject.response(400, 'Validation error')
  @appObj.flastRestPlusAPIObject.marshal_with(jobModel, code=201, description='Job created')
  @nsJobs.expect(jobModel, validate=True)
  def put(self):
    '''Create Job'''
    a = {
      'name': 'string',
      'name2': 'aa',
      'name3': 'string'
    }
    return a



appObj.flaskAppObject.register_blueprint(webfrontendBP, url_prefix='/frontend')

