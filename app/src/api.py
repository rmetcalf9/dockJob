from flask import Flask, Blueprint
from appObj import appObjClass
from flask_restplus import Api, Resource, fields, apidoc
import datetime
import pytz
app = Flask(__name__)
bp = Blueprint('dockjobapi', __name__, template_folder='dockjobapi')

from webfrontendAPI import webfrontendBP

appObj = appObjClass()

# I need to subclass this in order to change the url_prefix for swaggerui
#  so I can reverse proxy everyting under /apidocs
class SubclassRestPlusAPI(Api):
  def __init__(self, *args, reverse=False, **kwargs):
      super().__init__(*args, **kwargs)
  def _register_apidoc(self, app):
    conf = app.extensions.setdefault('restplus', {})
    if not conf.get('apidoc_registered', False):
      app.register_blueprint(apidoc.apidoc, url_prefix='/apidocs')
    conf['apidoc_registered'] = True


api = SubclassRestPlusAPI(app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API', doc='/'
)
apidocs_blueprint = Blueprint('api', __name__)
api.init_app(apidocs_blueprint)  
app.register_blueprint(apidocs_blueprint, url_prefix='/apidocs')

@bp.route('/serverinfo')
def serverinfo():
  curDatetime = datetime.datetime.now(pytz.utc)
  return appObj.getServerInfoJSON(curDatetime)

#Must register blueprints after the routes are declared
app.register_blueprint(bp, url_prefix='/dockjobapi')
app.register_blueprint(webfrontendBP, url_prefix='/dockjobfrontend')

