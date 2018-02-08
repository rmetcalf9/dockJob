from flask import Flask, Blueprint
from appObj import appObjClass
import datetime
import pytz
app = Flask(__name__)
bp = Blueprint('dockjobapi', __name__, template_folder='dockjobapi')

from webfrontendAPI import webfrontendBP

appObj = appObjClass()

@bp.route('/serverinfo')
def serverinfo():
  curDatetime = datetime.datetime.now(pytz.utc)
  return appObj.getServerInfoJSON(curDatetime)


#Must register blueprints after the routes are declared
app.register_blueprint(bp, url_prefix='/dockjobapi')
app.register_blueprint(webfrontendBP, url_prefix='/dockjobfrontend')

