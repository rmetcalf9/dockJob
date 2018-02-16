from flask import Flask, Blueprint
from appObj import appObjClass
from flask_restplus import Api, Resource, fields, apidoc
from FlaskRestSubclass import FlaskRestSubclass
import datetime
import pytz
app = Flask(__name__)
bp = Blueprint('dockjobapi', __name__, template_folder='dockjobapi')

from webfrontendAPI import webfrontendBP

appObj = appObjClass()

api = FlaskRestSubclass(app, version='1.0', title='TodoMVC API',
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

