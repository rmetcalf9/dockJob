# JobExecution represents a single execution of a Job
import datetime
import pytz
import uuid

class JobExecutionClass():
  guid = None
  stage = None  #Pending, Running, Completed
  dateCreated = None
  jobGUID = None
  jobCommand = None


  def __init__(self, job):
    self.guid = str(uuid.uuid4())
    self.stage = 'Pending'
    self.dateCreated = datetime.datetime.now(pytz.timezone("UTC"))
    self.jobGUID = job['GUID']
    self.jobCommand = job['command']


