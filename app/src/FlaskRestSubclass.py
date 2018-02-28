from flask_restplus import Api, apidoc, Swagger
import re
import json
from http import HTTPStatus

# http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/
# https://flask-restplus.readthedocs.io/en/stable/
# https://github.com/noirbizarre/flask-restplus



# I need to subclass this in order to change the url_prefix for swaggerui
#  so I can reverse proxy everything under /apidocs
class FlaskRestSubclass(Api):
  internalAPIPath = '/api'

  # Extra params inited manually
  apidocsurl = None 
  APIDOCSPath = None
  overrideAPIDOCSPath = None
  APIPath = None
  def setExtraParams(self, apidocsurl, APIDOCSPath, overrideAPIDOCSPath, APIPath):
    self.apidocsurl = apidocsurl
    self.APIDOCSPath = APIDOCSPath
    self.overrideAPIDOCSPath = overrideAPIDOCSPath
    self.APIPath = APIPath


  def __init__(self, *args, reverse=False, **kwargs):
      super().__init__(*args, **kwargs)
  def _register_apidoc(self, app):
    conf = app.extensions.setdefault('restplus', {})
    if not conf.get('apidoc_registered', False):
      apidoc.apidoc.add_url_rule('/swagger.json', None, self.getSwaggerJSON)
      app.register_blueprint(apidoc.apidoc, url_prefix='/apidocs')
    conf['apidoc_registered'] = True

  def reaplcements(self, res):
    regexp="\"https?:\/\/[a-zA-Z0\-9._]*(:[0-9]*)?" + self.internalAPIPath.replace("/","\/") + "\/swagger.json\""
    p = re.compile(regexp)
    res = p.sub("\"" + self.apidocsurl + "swagger.json\"", res)

    regexp="src=\"/apidocs/swaggerui/"
    p = re.compile(regexp)
    res = p.sub("src=\"" + self.APIDOCSPath + "/swaggerui/", res)
    regexp="href=\"/apidocs/swaggerui/"
    p = re.compile(regexp)
    res = p.sub("href=\"" + self.APIDOCSPath + "/swaggerui/", res)
    return res

  # Flask will serve the files with the url pointing at /apidocs.
  #  if I have my reverse proxy serving it somewhere else I need to alter this
  def render_doc(self):
    '''Override this method to customize the documentation page'''
    if self._doc_view:
      return self._doc_view()
    elif not self._doc:
      self.abort(HTTPStatus.NOT_FOUND)
    res = apidoc.ui_for(self)
    if (self.overrideAPIDOCSPath()):
      #print("About to replace")
      #print(res)
      res = self.reaplcements(res)
      #print("Replaced")
      #print(res)
      #print("End")
    return res

  #By default swagger.json is registered as /api/swagger.json
  # as this is security protected I need this to be accessed in /apidocs/swagger.json as well
  def getSwaggerJSON(self):
    schema = self.__schema__
    return json.dumps(schema), HTTPStatus.INTERNAL_SERVER_ERROR if 'error' in schema else HTTPStatus.OK, {'Content-Type': 'application/json'}

  #Override the basepath given in the swagger file
  # I need to give out a different one from where the endpoint is registered
  @property
  def base_path(self):
    '''
    The API path
    :rtype: str
    '''
    return self.APIPath


