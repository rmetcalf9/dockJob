from .ExternalTriggerTypes import getAllTriggerTypeInstances
from .api import register_api

class ExternalTriggerManager():
    DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD = None
    TriggerTypes = None
    def __init__(self, DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD):
        self.DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD = DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD
        self.TriggerTypes = getAllTriggerTypeInstances()

    def getStaticServerInfoData(self):
        types = {}
        for type in self.TriggerTypes:
            types[type] = self.TriggerTypes[type].getStaticServerInfoData()
        return {
            "types": types
        }

