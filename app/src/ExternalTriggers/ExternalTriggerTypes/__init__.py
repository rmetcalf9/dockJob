from .googleDriveRaw import googleDriveRawClass
from .googleDriveNewFileWatch import googleDriveNewFileWatchClass

def getAllTriggerTypeInstances(externalTriggerManager):
    retVal = {}
    triggerType = googleDriveRawClass(externalTriggerManager)
    retVal[triggerType.__class__.__name__] = triggerType
    triggerType = googleDriveNewFileWatchClass(externalTriggerManager)
    retVal[triggerType.__class__.__name__] = triggerType
    return retVal
