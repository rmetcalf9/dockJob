from flask_restplus import Api, apidoc
from GlobalParamaters import GlobalParamaters
import re

# I need to subclass this in order to change the url_prefix for swaggerui
#  so I can reverse proxy everything under /apidocs
class FlaskRestSubclass(Api):
  def __init__(self, *args, reverse=False, **kwargs):
      super().__init__(*args, **kwargs)
  def _register_apidoc(self, app):
    conf = app.extensions.setdefault('restplus', {})
    if not conf.get('apidoc_registered', False):
      app.register_blueprint(apidoc.apidoc, url_prefix='/apidocs')
    conf['apidoc_registered'] = True

  def reaplcements(self, res):
    #res = res.replace('/apidocs/',GlobalParamaters.get().getAPIDOCSPath() + '/')
    #regexp="\"https?:\/\/[a-zA-Z0\-9._]*(:[0-9]*)?/apidocs/swagger.json\""
    regexp="\"https?:\/\/[a-zA-Z0\-9._]*(:[0-9]*)?\/apidocs/swagger.json\""
    p = re.compile(regexp)
    res = p.sub("\"" + GlobalParamaters.get().apidocsurl + "swagger.json\"", res)
    regexp="src=\"/apidocs/swaggerui/"
    p = re.compile(regexp)
    res = p.sub("src=\"" + GlobalParamaters.get().getAPIDOCSPath() + "/swaggerui/", res)
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
    if (GlobalParamaters.get().overrideAPIDOCSPath()):
      print("About to replace")
      print(res)
      res = self.reaplcements(res)
      print("Replaced")
      print(res)
      print("End")
    return res

