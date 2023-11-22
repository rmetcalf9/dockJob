from .googleDriveRaw import googleDriveRawClass
from .googleDriveNewFileWatch import googleDriveNewFileWatchClass

def getAllTriggerTypeInstances(externalTriggerManager):
    retVal = {}
    triggerType = googleDriveRawClass(externalTriggerManager, googleDriveRawClass.__name__)
    retVal[triggerType.getTypeName()] = triggerType
    triggerType = googleDriveNewFileWatchClass(externalTriggerManager, googleDriveNewFileWatchClass.__name__)
    retVal[triggerType.getTypeName()] = triggerType

    return retVal
