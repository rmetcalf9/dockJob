

data_simpleJobCreateParams = {
  "name": "TestJob",
  "repetitionInterval": "HOURLY:03",
  "command": "ls",
  "enabled": True
}
data_simpleManualJobCreateParams = {
  "name": "TestJob",
  "repetitionInterval": "",
  "command": "ls",
  "enabled": False
}
data_simpleJobCreateExpRes = {
  "guid": 'IGNORE', 
  "name": data_simpleJobCreateParams['name'], 
  "command": data_simpleJobCreateParams['command'], 
  "enabled": data_simpleJobCreateParams['enabled'], 
  "repetitionInterval": data_simpleJobCreateParams['repetitionInterval'], 
  "nextScheduledRun": 'IGNORE', 
  "creationDate": "IGNORE", 
  "lastUpdateDate": "IGNORE",
  "lastRunDate": None,
  "lastRunReturnCode": None,
  "lastRunExecutionGUID": "",
  "mostRecentCompletionStatus": "Unknown",
  "pinned": False,
  "overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown": None,
  "AfterFailJobGUID": None,
  "AfterFailJobNAME": None,
  "AfterSuccessJobGUID": None,
  "AfterSuccessJobNAME": None,
  "AfterUnknownJobGUID": None,
  "AfterUnknownJobNAME": None,
  "StateChangeSuccessJobGUID": None,
  "StateChangeSuccessJobNAME": None,
  "StateChangeFailJobGUID": None,
  "StateChangeFailJobNAME": None,
  "StateChangeUnknownJobGUID": None,
  "StateChangeUnknownJobNAME": None,
  "objectVersion": 1,
  "ExternalTrigger": {"triggerActive": False}
}

data_simpleManualJobCreateParamsWithAllOptionalFields = dict(data_simpleJobCreateParams)
data_simpleManualJobCreateParamsWithAllOptionalFields['pinned'] = True
data_simpleManualJobCreateParamsWithAllOptionalFields['overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown'] = 357
data_simpleManualJobCreateParamsWithAllOptionalFields['StateChangeSuccessJobGUID'] = '' #Can't provide valid non default value as other jobs don't exist
data_simpleManualJobCreateParamsWithAllOptionalFields['StateChangeFailJobGUID'] = '' #
data_simpleManualJobCreateParamsWithAllOptionalFields['StateChangeUnknownJobGUID'] = '' #

data_simpleManualJobCreateParamsWithAllOptionalFieldsExpRes = dict(data_simpleJobCreateExpRes)
data_simpleManualJobCreateParamsWithAllOptionalFieldsExpRes['pinned'] = True
data_simpleManualJobCreateParamsWithAllOptionalFieldsExpRes['overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown'] = 357

data_simpleJobExecutionCreateExpRes = {
  "guid": 'IGNORE',
  "stage": 'Pending', 
  "executionName": 'TestExecutionName', 
  "resultReturnCode": 0, 
  "jobGUID": 'OVERRIDE',
  "jobName": 'TestJob',
  "jobCommand": 'OVERRIDE',
  "resultSTDOUT": '', 
  "manual": True, 
  "dateCreated": 'IGNORE', 
  "dateStarted": 'IGNORE', 
  "dateCompleted": 'IGNORE' 
}


