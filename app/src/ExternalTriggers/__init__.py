from .ExternalTriggerTypes import getAllTriggerTypeInstances


class ExternalTriggerManager():
    DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD = None
    def __init__(self, DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD):
        self.DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD = DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD
