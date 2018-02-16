from flask import Flask, Blueprint
from appObj import appObjClass
from flask_restplus import Api, Resource, fields, apidoc
from GlobalParamaters import GlobalParamaters
import datetime
import pytz
app = Flask(__name__)
bp = Blueprint('dockjobapi', __name__, template_folder='dockjobapi')

from webfrontendAPI import webfrontendBP

appObj = appObjClass()

# I need to subclass this in order to change the url_prefix for swaggerui
#  so I can reverse proxy everything under /apidocs
class SubclassRestPlusAPI(Api):
  def __init__(self, *args, reverse=False, **kwargs):
      super().__init__(*args, **kwargs)
  def _register_apidoc(self, app):
    conf = app.extensions.setdefault('restplus', {})
    if not conf.get('apidoc_registered', False):
      app.register_blueprint(apidoc.apidoc, url_prefix='/apidocs')
    conf['apidoc_registered'] = True
  # Flask will serve the files with the url pointing at /apidocs.
  #  if I have my reverse proxy serving it somewhere else I need to alter this
  def render_doc(self):
    '''Override this method to customize the documentation page'''
    if self._doc_view:
      return self._doc_view()
    elif not self._doc:
      self.abort(HTTPStatus.NOT_FOUND)
    res = apidoc.ui_for(self)
    if (GlobalParamaters.get().overrideAPIDOCSPath()):
      print("About to replace")
      print(res)
      res = res.replace('/apidocs/',GlobalParamaters.get().getAPIDOCSPath() + '/')
      print("Replaced")
      print(res)
      print("End")
    return res

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

