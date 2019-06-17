from jobObj import jobClass

#I need jobs to be stored in order so pagination works
from sortedcontainers import SortedDict

from werkzeug.exceptions import BadRequest

objectType = "jobsData"

# One instance of this class is held by the appObj
# this class keeps track of all the jobObjects

class jobsDataClass():
  # map of Jobs keyed by GUID
  jobs = None
  # map of Job name to guid
  jobs_name_lookup = None
  appObj = None

  def __init__(self, appObj):
    self.jobs = SortedDict()
    self.jobs_name_lookup = SortedDict()
    self.appObj = appObj

  #Called by appObj when the program is started and objectstore is setup
  def loadFromObjectStore(self):
    storeConnection = self.appObj.objectStore._getConnectionContext()
    def someFn(connectionContext):
      paginatedParamValues = {
        'offset': 0,
        'pagesize': 100000,
        'query': '',
        'sort': '',
      }
      loadedData = connectionContext.getPaginatedResult(objectType, paginatedParamValues=paginatedParamValues, outputFN=None)
      print(loadedData)
      print("Found " + str(len(loadedData["result"])) + " jobs in datastore")
      for curRecord in loadedData["result"]:
        print(curRecord)
        # call init Job Obj
        #call _addJob(self, job)
        raise Exception("Load data Not Implemented")
        
    storeConnection.executeInsideTransaction(someFn)  
  

  def _saveJobToObjectStore(self, jobGUID):
    storeConnection = self.appObj.objectStore._getConnectionContext()
    def someFn(connectionContext):
      #print(self.jobs[jobGUID]._caculatedDict(self.appObj))
      newObjectVersion = connectionContext.saveJSONObject(objectType, jobGUID, self.jobs[jobGUID]._caculatedDict(self.appObj), objectVersion = self.jobs[jobGUID].objectVersion)
      self.jobs[jobGUID].objectVersion = newObjectVersion
    storeConnection.executeInsideTransaction(someFn)  

    
  def _deleteJobFromObjectStore(self, jobGUID, objectVersion):
    storeConnection = self.appObj.objectStore._getConnectionContext()
    def someFn(connectionContext):
      connectionContext.removeJSONObject(objectType, jobGUID, objectVersion = objectVersion, ignoreMissingObject = False)
    storeConnection.executeInsideTransaction(someFn)  

  #Run Job loop iteration
  def loopIteration(self, appObj, curTime):
    for jobIdx in self.jobs:
      self.jobs[jobIdx].loopIteration(appObj, curTime)

  def getJobServerInfo(self):
    nextJobToExecute = self.getNextJobToExecute()

    # Find Job stats
    JobsNeverRun = 0
    JobsCompletingSucessfully = 0
    JobsLastExecutionFailed = 0
    for jobIdx in self.jobs:
      if self.jobs[jobIdx].lastRunReturnCode is None:
        JobsNeverRun += 1
      else:
        if self.jobs[jobIdx].lastRunReturnCode == 0:
          JobsCompletingSucessfully += 1
        else:
          JobsLastExecutionFailed += 1

    if nextJobToExecute is None:
      xx = []
    else:
      xx = [nextJobToExecute]
    return{
      'TotalJobs': len(self.jobs),
      'NextJobsToExecute': xx,
      'JobsNeverRun': JobsNeverRun,
      'JobsCompletingSucessfully': JobsCompletingSucessfully,
      'JobsLastExecutionFailed': JobsLastExecutionFailed
    }
    
  def getJob(self, guid):
    try:
      r = self.jobs[str(guid)]
    except KeyError:
      raise BadRequest('Invalid Job GUID')
    return r
  def getJobByName(self, name):
    return self.jobs[str(self.jobs_name_lookup[jobClass.uniqueJobNameStatic(name)])]

  # Adds job to internal structures but not objectstore
  def _addJob(self, job):
    uniqueJobName = job.uniqueName()
    if (str(job.guid) in self.jobs):
      return {'msg': 'GUID already in use', 'guid':''}
    if (uniqueJobName in self.jobs_name_lookup):
      return {'msg': 'Job Name already in use - ' + uniqueJobName, 'guid':''}
    self.jobs[str(job.guid)] = job
    self.jobs_name_lookup[uniqueJobName] = job.guid
    self.nextJobToExecuteCalcRequired = True
    return {'msg': 'OK', 'guid':job.guid}


  # return GUID or error
  def addJob(self, job):
    retVal = self._addJob(job)
    if retVal['msg']=='OK':
      self._saveJobToObjectStore(str(retVal['guid']))
    return retVal

  def updateJob(self, jobObj, newValues):
    jobClass.assertValidName(newValues['name'])
    jobClass.assertValidRepetitionInterval(newValues['repetitionInterval'], newValues['enabled'])

    oldUniqueJobName = jobObj.uniqueName()
    newUniqueJobName = jobClass.uniqueJobNameStatic(newValues['name'])
    if (str(jobObj.guid) not in self.jobs):
      raise Exception('Job to update dose not exist')
    if (oldUniqueJobName not in self.jobs_name_lookup):
      raise Exception('Old Job Name does not exist')

    # Only change the name lookup if there actually is a change
    if oldUniqueJobName != newUniqueJobName:
      if (newUniqueJobName in self.jobs_name_lookup):
        raise Exception('New Job Name already in use')
      # remove old unique name lookup
      tmpVar = self.jobs_name_lookup.pop(oldUniqueJobName)
      if tmpVar is None:
        raise Execption('Failed to remove old unique name')
      # add new unique lookup
      self.jobs_name_lookup[newUniqueJobName] = jobObj.guid

    # set recaculation of repetition interval values
    if jobObj.repetitionInterval != newValues['repetitionInterval']:
      self.nextJobToExecuteCalcRequired = True
    if jobObj.enabled != newValues['enabled']:
      self.nextJobToExecuteCalcRequired = True

    # change values in object to new values
    jobObj.setNewValues(
      self.appObj,
      newValues['name'],
      newValues['command'],
      newValues['enabled'],
      newValues['repetitionInterval'],
      newValues.get('pinned',False), 
      newValues.get('overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown',None),
      newValues.get('StateChangeSuccessJobGUID',None),
      newValues.get('StateChangeFailJobGUID',None),
      newValues.get('StateChangeUnknownJobGUID',None)
    )
    self._saveJobToObjectStore(str(jobObj.guid))


  def deleteJob(self, jobObj):
    objectVersionOfObjectToDelete = jobObj.objectVersion
    uniqueJobName = jobObj.uniqueName()
    tmpVar = self.jobs_name_lookup.pop(uniqueJobName)
    if tmpVar is None:
      raise Execption('Failed to delete a job could not get it out of the job name lookup')
    tmpVar2 = self.jobs.pop(jobObj.guid)
    if tmpVar2 is None:
      raise Execption('Failed to delete a job could not get it out of the jobs')
    # Delete any executions
    self.appObj.jobExecutor.deleteExecutionsForJob(jobObj.guid)
    # If it is next to execute we need to recaculate
    if self.nextJobToExecute != None:
      if jobObj.guid == self.nextJobToExecute.guid:
        self.nextJobToExecuteCalcRequired = True
    self._deleteJobFromObjectStore(str(jobObj.guid), objectVersionOfObjectToDelete)

  #nextJobToExecute holds the next job scheduled to execute
  # When ever any actions are preformed that may change this the CalcRequired flag is set to true
  # the get function will either return or recaculate as desired
  # Changing actions:
  #  - Adding Job
  #  - Delete job if it is the next to execute
  #  - Executing a job
  #  - Editing a job
  # None is a valid next job to execute but when it 
  nextJobToExecute = None
  nextJobToExecuteCalcRequired = True
  def getNextJobToExecute(self):
    if not self.nextJobToExecuteCalcRequired:
      return self.nextJobToExecute
    self.nextJobToExecute = None
    for jobIdx in self.jobs:
      if self.jobs[jobIdx].nextScheduledRun is not None:
        if self.nextJobToExecute is None:
          self.nextJobToExecute = self.jobs[jobIdx]
        else:
          if self.jobs[jobIdx].nextScheduledRun < self.nextJobToExecute.nextScheduledRun:
            self.nextJobToExecute = self.jobs[jobIdx]
    self.nextJobToExecuteCalcRequired = False
    return self.nextJobToExecute

  def registerRunDetails(self, jobGUID, newLastRunDate, newLastRunReturnCode, triggerExecutionObj):
    self.jobs[str(jobGUID)].registerRunDetails(self.appObj, newLastRunDate, newLastRunReturnCode, triggerExecutionObj)

  #function for testing allowing us to pretend it is currently a different time
  def recaculateExecutionTimesBasedonNewTime(self, curTime):
    for jobIdx in self.jobs:
      self.jobs[jobIdx].setNextScheduledRun(curTime)
    self.nextJobToExecuteCalcRequired = True

