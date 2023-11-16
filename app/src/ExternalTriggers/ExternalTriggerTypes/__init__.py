from .googleDriveRaw import googleDriveRawClass
from .googleDriveNewFileWatch import googleDriveNewFileWatchClass

def getAllTriggerTypeInstances():
    retVal = {}
    triggerType = googleDriveRawClass()
    retVal[triggerType.__class__.__name__] = triggerType
    triggerType = googleDriveNewFileWatchClass()
    retVal[triggerType.__class__.__name__] = triggerType
    return retVal
