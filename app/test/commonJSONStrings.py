

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
  "overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown": None
}

data_simpleJobExecutionCreateExpRes = {
  "guid": 'IGNORE',
  "stage": 'Pending', 
  "executionName": 'TestExecutionName', 
  "resultReturnCode": 0, 
  "jobGUID": 'OVERRIDE',
  "jobCommand": 'OVERRIDE',
  "resultSTDOUT": '', 
  "manual": True, 
  "dateCreated": 'IGNORE', 
  "dateStarted": 'IGNORE', 
  "dateCompleted": 'IGNORE' 
}


