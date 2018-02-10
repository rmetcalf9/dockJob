from flask import Blueprint, send_from_directory
from appObj import appObjClass
from GlobalParamaters import GlobalParamaters
webfrontendBP = Blueprint('webfrontend', __name__, template_folder='webfrontend')
from GlobalParamaters import GlobalParamaters

# API used to server the quasar application directly
# see https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask

##appObj = appObjClass()

@webfrontendBP.route('/<path:path>')
def normalfile(path):
  return send_from_directory(GlobalParamaters.get().getWebFrontendPath() + '/', path)

@webfrontendBP.route('/')
def missingfile():
  print("webfrontend acces with no file - returning index.html")
  return normalfile('index.html')

@webfrontendBP.route('/webfrontendConnectionData')
def dynamicfile():
  return GlobalParamaters.get().getWebServerInfoJSON()

