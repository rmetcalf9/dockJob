from flask import Flask
from appObj import appObjClass
import datetime
import pytz
app = Flask(__name__)


appObj = appObjClass()

@app.route('/serverinfo')
def serverinfo():
  curDatetime = datetime.datetime.now(pytz.utc)
  return appObj.getServerInfoJSON(curDatetime)

