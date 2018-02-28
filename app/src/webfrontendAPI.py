from flask import Blueprint, send_from_directory
webfrontendBP = Blueprint('webfrontend', __name__, template_folder='webfrontend')

# API used to server the quasar application directly
# see https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask

def registerAPI(appObj):
  @webfrontendBP.route('/<path:path>')
  def normalfile(path):
    if appObj.globalParamObject.getWebFrontendPath()=='_':
      raise Exception('Running with blank webfrontend but trying to access frontend through python app')
    return send_from_directory(appObj.globalParamObject.getWebFrontendPath() + '/', path)

  @webfrontendBP.route('/')
  def missingfile():
    print("webfrontend acces with no file - returning index.html")
    return normalfile('index.html')

  @webfrontendBP.route('/webfrontendConnectionData')
  def dynamicfile():
    return appObj.globalParamObject.getWebServerInfoJSON()

