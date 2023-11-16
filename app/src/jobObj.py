import datetime
from werkzeug.exceptions import BadRequest
import pytz
import uuid
from threading import Lock
from dateutil.relativedelta import relativedelta
from RepetitionInterval import RepetitionIntervalClass

class jobFactoryClass():
  def loadFromDB(self, jobFromDBTuple, appObj):
    jobFromDB = jobFromDBTuple[0]
    repetitionInterval = jobFromDB["repetitionInterval"]

    fieldsToDefaultToNone = ["AfterSuccessJobGUID", "AfterFailJobGUID", "AfterUnknownJobGUID"]
    for fieldToDefault in fieldsToDefaultToNone:
      if fieldToDefault not in jobFromDB:
        jobFromDB[fieldToDefault] = None

    if "PrivateExternalTrigger" not in jobFromDB:
      jobFromDB["PrivateExternalTrigger"] = {
        "triggerActive": False
      }

    return jobClass(
      appObj = appObj,
      name = jobFromDB["name"],
      command = jobFromDB["command"],
      enabled = jobFromDB["enabled"],
      repetitionInterval = repetitionInterval,
      pinned = jobFromDB["pinned"],
      overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown = jobFromDB["overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown"],
      StateChangeSuccessJobGUID = jobFromDB["StateChangeSuccessJobGUID"],
      StateChangeFailJobGUID = jobFromDB["StateChangeFailJobGUID"],
      StateChangeUnknownJobGUID = jobFromDB["StateChangeUnknownJobGUID"],
      AfterSuccessJobGUID = jobFromDB["AfterSuccessJobGUID"],
      AfterFailJobGUID = jobFromDB["AfterFailJobGUID"],
      AfterUnknownJobGUID = jobFromDB["AfterUnknownJobGUID"],
      guid = jobFromDB["guid"],
      loadingObjectVersion = jobFromDBTuple[1],
      PrivateExternalTrigger = jobFromDB["PrivateExternalTrigger"],
      verifyDependentJobGuids = True
  )

jobFactory = jobFactoryClass()


#Class to represent a job
class jobClass():
  guid = None
  name = None
  command = None
  enabled = None
  repetitionInterval = None
  creationDate = None
  lastUpdateDate = None
  lastRunDate = None
  nextScheduledRun = None
  lastRunReturnCode = None
  lastRunExecutionGUID = None
  pinned = False
  overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown = None
  mostRecentCompletionStatus = 'Unknown'
  resetCompletionStatusToUnknownTime = None
  StateChangeSuccessJobGUID = None
  StateChangeFailJobGUID = None
  StateChangeUnknownJobGUID = None
  AfterSuccessJobGUID =None
  AfterFailJobGUID = None
  AfterUnknownJobGUID = None
  PrivateExternalTrigger = None

  CompletionstatusLock = None
  objectVersion = None

  def __repr__(self):
    ret = 'jobClass('
    ret += 'guid:' + self.guid + ' '
    ret += 'name:' + self.name + ' '
    ret += 'command:' + self.command + ' '
    ret += 'enabled:' + str(self.enabled) + ' '
    ret += 'repetitionInterval:' + self.repetitionInterval + ' '
    ret += 'creationDate:' + str(self.creationDate) + ' '
    ret += 'lastRunReturnCode:' + str(self.lastRunReturnCode) + ' '
    ret += 'lastRunExecutionGUID:' + str(self.lastRunExecutionGUID) + ' '
    ret += ')'
    return ret

  def assertValidName(name):
    if (len(name)<2):
      raise BadRequest('Job name must be more than 2 characters')
  def assertValidRepetitionInterval(ri, enabled):
    if ri is None:
      ri = ''
    if ri == '':
      if enabled:
        raise BadRequest('Repetition interval not set but enabled is true')
      return None
    try:
      return RepetitionIntervalClass(ri)
    except:
      raise BadRequest('Invalid Repetition Interval')

  def setNewRepetitionInterval(self, newRepetitionInterval):
    self.repetitionInterval = newRepetitionInterval
    if (self.repetitionInterval != None):
      if (self.repetitionInterval != ''):
        ri = RepetitionIntervalClass(self.repetitionInterval)
        self.repetitionInterval = ri.__str__()

  def verifyJobGUID(self, appObj, jobGUID, callingJobGUID):
    if jobGUID is None:
      return None
    if jobGUID == '':
      return None
    if callingJobGUID == jobGUID:
      raise BadRequest('A follow on action can not be set to the same job')
    unused = appObj.appData['jobsData'].getJob(jobGUID) #Will throw bad request exception if job dosen't exist
    return jobGUID

  def __init__(
      self,
      appObj,
      name,
      command,
      enabled,
      repetitionInterval,
      pinned,
      overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown,
      StateChangeSuccessJobGUID,
      StateChangeFailJobGUID,
      StateChangeUnknownJobGUID,
      AfterSuccessJobGUID,
      AfterFailJobGUID,
      AfterUnknownJobGUID,
      guid, #used when loading from DB
      verifyDependentJobGuids, #False when testing
      loadingObjectVersion, #used when loading from DB
      PrivateExternalTrigger
  ):
    jobClass.assertValidName(name)
    jobClass.assertValidRepetitionInterval(repetitionInterval, enabled)
    curTime = datetime.datetime.now(pytz.timezone("UTC"))
    if guid is None:
      self.guid = str(uuid.uuid4())
    else:
      self.guid = guid
    self.name = name
    self.command = command
    self.enabled = enabled
    self.setNewRepetitionInterval(repetitionInterval)
    self.creationDate = curTime.isoformat()
    self.lastUpdateDate = curTime.isoformat()
    self.lastRunDate = None
    self.lastRunExecutionGUID = ''
    self.lastRunReturnCode = None
    self.nextScheduledRun = None
    self.setNextScheduledRun(datetime.datetime.now(pytz.timezone("UTC")))
    self.pinned = pinned
    if overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown == 0:
      overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown = None
    self.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown = overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown
    self.mostRecentCompletionStatus = 'Unknown'
    if verifyDependentJobGuids:
      self.StateChangeSuccessJobGUID = self.verifyJobGUID(appObj, StateChangeSuccessJobGUID, self.guid)
      self.StateChangeFailJobGUID = self.verifyJobGUID(appObj, StateChangeFailJobGUID, self.guid)
      self.StateChangeUnknownJobGUID = self.verifyJobGUID(appObj, StateChangeUnknownJobGUID, self.guid)
      self.AfterSuccessJobGUID = self.verifyJobGUID(appObj, AfterSuccessJobGUID, self.guid)
      self.AfterFailJobGUID = self.verifyJobGUID(appObj, AfterFailJobGUID, self.guid)
      self.AfterUnknownJobGUID = self.verifyJobGUID(appObj, AfterUnknownJobGUID, self.guid)
    else:
      self.StateChangeSuccessJobGUID = StateChangeSuccessJobGUID
      self.StateChangeFailJobGUID = StateChangeFailJobGUID
      self.StateChangeUnknownJobGUID = StateChangeUnknownJobGUID
      self.AfterSuccessJobGUID = AfterSuccessJobGUID
      self.AfterFailJobGUID = AfterFailJobGUID
      self.AfterUnknownJobGUID = AfterUnknownJobGUID

    #fields excluded from JSON output
    self.resetCompletionStatusToUnknownTime = None
    self.CompletionstatusLock = Lock()

    self.PrivateExternalTrigger = PrivateExternalTrigger

    self.objectVersion = loadingObjectVersion

  def _getMinutesBeforeMostRecentCompletionStatusBecomesUnknown(self, appObj):
    if self.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown == None:
      return appObj.minutesBeforeMostRecentCompletionStatusBecomesUnknown
    return self.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown

  def _getCaculatedValueForModeRecentCompletionStatus(self, appObj, lastRunDate, lastRunReturnCode):
    if lastRunDate is None:
      return "Unknown"
    earlyTime = appObj.getCurDateTime() - relativedelta(minutes=self._getMinutesBeforeMostRecentCompletionStatusBecomesUnknown(appObj))
    if lastRunDate < earlyTime:
      return "Unknown"
    if lastRunReturnCode==0:
      return "Success"
    else:
      return "Fail"

  def _caculatedDictWithoutAppObjDependancy(self):
    ret = dict(self.__dict__)
    del ret['PrivateExternalTrigger']
    del ret['CompletionstatusLock']
    del ret['resetCompletionStatusToUnknownTime']
    if self.lastRunDate is not None:
      ret['lastRunDate'] = self.lastRunDate.isoformat()

    # If there is no state change job set the value returned should be null
    ret['StateChangeSuccessJobNAME'] = None
    ret['StateChangeFailJobNAME'] = None
    ret['StateChangeUnknownJobNAME'] = None
    ret['AfterSuccessJobNAME'] = None
    ret['AfterFailJobNAME'] = None
    ret['AfterUnknownJobNAME'] = None

    return ret

  # Needed when we use extra caculated values in the dict
  def _caculatedDict(self, appObj):
    ret = self._caculatedDictWithoutAppObjDependancy()

    if self.StateChangeSuccessJobGUID is not None:
      ret['StateChangeSuccessJobNAME'] = appObj.appData['jobsData'].getJob(self.StateChangeSuccessJobGUID).name
    if self.StateChangeFailJobGUID is not None:
      ret['StateChangeFailJobNAME'] = appObj.appData['jobsData'].getJob(self.StateChangeFailJobGUID).name
    if self.StateChangeUnknownJobGUID is not None:
      ret['StateChangeUnknownJobNAME'] = appObj.appData['jobsData'].getJob(self.StateChangeUnknownJobGUID).name
    if self.AfterSuccessJobGUID is not None:
      ret['AfterSuccessJobNAME'] = appObj.appData['jobsData'].getJob(self.AfterSuccessJobGUID).name
    if self.AfterFailJobGUID is not None:
      ret['AfterFailJobNAME'] = appObj.appData['jobsData'].getJob(self.AfterFailJobGUID).name
    if self.AfterUnknownJobGUID is not None:
      ret['AfterUnknownJobNAME'] = appObj.appData['jobsData'].getJob(self.AfterUnknownJobGUID).name

    ret["ExternalTrigger"] = appObj.externalTriggerManager.getJobDictData(self)

    return ret

  def setNewValues(
    self,
    appObj,
    name,
    command,
    enabled,
    repetitionInterval,
    pinned,
    overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown,
    StateChangeSuccessJobGUID,
    StateChangeFailJobGUID,
    StateChangeUnknownJobGUID,
    AfterSuccessJobGUID,
    AfterFailJobGUID,
    AfterUnknownJobGUID
  ):
    self.name = name
    self.command = command
    self.enabled = enabled
    self.setNewRepetitionInterval(repetitionInterval)
    self.setNextScheduledRun(datetime.datetime.now(pytz.timezone("UTC")))
    self.pinned = pinned
    if overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown==0:
      overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown = None
    self.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown = overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown
    self.StateChangeSuccessJobGUID = self.verifyJobGUID(appObj, StateChangeSuccessJobGUID, self.guid)
    self.StateChangeFailJobGUID = self.verifyJobGUID(appObj, StateChangeFailJobGUID, self.guid)
    self.StateChangeUnknownJobGUID = self.verifyJobGUID(appObj, StateChangeUnknownJobGUID, self.guid)
    self.AfterSuccessJobGUID = self.verifyJobGUID(appObj, AfterSuccessJobGUID, self.guid)
    self.AfterFailJobGUID = self.verifyJobGUID(appObj, AfterFailJobGUID, self.guid)
    self.AfterUnknownJobGUID = self.verifyJobGUID(appObj, AfterUnknownJobGUID, self.guid)

  def removeRemoveRelianceOnOtherJob(self, guid):
    # return True if a change is made
    changed = False
    if self.StateChangeSuccessJobGUID == guid:
      self.StateChangeSuccessJobGUID = None
      changed = True
    if self.StateChangeFailJobGUID == guid:
      self.StateChangeFailJobGUID = None
      changed = True
    if self.StateChangeUnknownJobGUID == guid:
      self.StateChangeUnknownJobGUID = None
      changed = True
    if self.AfterSuccessJobGUID == guid:
      self.AfterSuccessJobGUID = None
      changed = True
    if self.AfterFailJobGUID == guid:
      self.AfterFailJobGUID = None
      changed = True
    if self.AfterUnknownJobGUID == guid:
      self.AfterUnknownJobGUID = None
      changed = True

    return changed

  def setNextScheduledRun(self, curTime):
    ri = None
    if self.enabled == False:
      self.nextScheduledRun = None
    else:
      if (self.repetitionInterval != None):
        if (self.repetitionInterval != ''):
          ri = RepetitionIntervalClass(self.repetitionInterval)
          self.nextScheduledRun = ri.getNextOccuranceDatetime(curTime).isoformat()

  def uniqueJobNameStatic(name):
    return name.strip().upper()

  def uniqueName(self):
    return jobClass.uniqueJobNameStatic(self.name)


  def _startPostCompletionJob(self, jobGuid, eventName, triggerExecutionObj, appObj):
    #Send a post completion event
    appObj.jobExecutor.submitJobForExecution(
      jobGuid,
      executionName='Event - ' + eventName,
      manual=False,
      triggerJobObj=self,
      triggerEvent=eventName,
      callerHasJobExecutionLock=True,
      triggerExecutionObj=triggerExecutionObj
    )

  #Called from job execution thread and request processing threads
  def _setNewCompletionStatus(self, appObj, newStatus, triggerExecutionObj):
    if self.mostRecentCompletionStatus == newStatus:
      if newStatus == 'Success':
        if self.AfterSuccessJobGUID is not None:
          self._startPostCompletionJob(self.AfterSuccessJobGUID, "AfterSuccess", triggerExecutionObj, appObj)
      elif newStatus == 'Fail':
        if self.AfterFailJobGUID is not None:
          self._startPostCompletionJob(self.AfterFailJobGUID, "AfterFail", triggerExecutionObj, appObj)
      else:
        if self.AfterUnknownJobGUID is not None:
          self._startPostCompletionJob(self.AfterUnknownJobGUID, "AfterUnknown", triggerExecutionObj, appObj)
      return
    self.CompletionstatusLock.acquire()
    self.mostRecentCompletionStatus = newStatus
    self.CompletionstatusLock.release()
    if newStatus=='Success':
      if self.StateChangeSuccessJobGUID is not None:
        self._startPostCompletionJob(self.StateChangeSuccessJobGUID, "StateChangeToSuccess", triggerExecutionObj, appObj)
      else:
        if self.AfterSuccessJobGUID is not None:
          self._startPostCompletionJob(self.AfterSuccessJobGUID, "AfterSuccess", triggerExecutionObj, appObj)
    elif newStatus=='Fail':
      if self.StateChangeFailJobGUID is not None:
        self._startPostCompletionJob(self.StateChangeFailJobGUID, "StateChangeToFail", triggerExecutionObj, appObj)
      else:
        if self.AfterFailJobGUID is not None:
          self._startPostCompletionJob(self.AfterFailJobGUID, "AfterFail", triggerExecutionObj, appObj)
    else:
      if self.StateChangeUnknownJobGUID is not None:
        self._startPostCompletionJob(self.StateChangeUnknownJobGUID, "StateChangeToUnknown", triggerExecutionObj, appObj)
      else:
        if self.AfterUnknownJobGUID is not None:
          self._startPostCompletionJob(self.AfterUnknownJobGUID, "AfterUnknown", triggerExecutionObj, appObj)

  def registerRunDetails(self, appObj, newLastRunDate, newLastRunReturnCode, triggerExecutionObj):
    #print('registerRunDetails for job ' + self.name + ' - lastrundate=' + newLastRunDate.isoformat())
    self.lastRunDate = newLastRunDate
    self.lastRunReturnCode = newLastRunReturnCode
    self.lastRunExecutionGUID = triggerExecutionObj.guid
    self.resetCompletionStatusToUnknownTime = newLastRunDate + relativedelta(minutes=self._getMinutesBeforeMostRecentCompletionStatusBecomesUnknown(appObj))

    newCompletionStatus = self._getCaculatedValueForModeRecentCompletionStatus(appObj, lastRunDate=newLastRunDate, lastRunReturnCode=newLastRunReturnCode)
    self._setNewCompletionStatus(
      appObj=appObj,
      newStatus=newCompletionStatus,
      triggerExecutionObj=triggerExecutionObj
    )

  #In the loop each job needs to check if its status needs to become unknown
  # this is required because the job may need to emit an event as a result
  # This is called from the job execution thread
  def loopIteration(self, appObj, curTime):
    if self.mostRecentCompletionStatus == 'Unknown':
      return
    if curTime > self.resetCompletionStatusToUnknownTime:
      self._setNewCompletionStatus(
        appObj=appObj,
        newStatus='Unknown',
        triggerExecutionObj=None
      )

