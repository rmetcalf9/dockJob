
class externalTriggerBaseClass():
    externalTriggerManager = None
    def __init__(self, externalTriggerManager):
        self.externalTriggerManager = externalTriggerManager
    def getStaticServerInfoData(self):
        return {}

    def getEncodedJobGuidFromMessage(self, urlid, request_headers, request_data):
        return None

    def requestMatches(self, jobData, urlid, request_headers, request_data, rawurlpasscode, rawnonurlpasscode):
        return False

    # Return value (updateJobNeeded, typeprivatevars, typepublicvars)
    def fireTrigger(self, submitJobFunction, jobData, urlid, request_headers, request_data, rawurlpasscode, rawnonurlpasscode):
        submitJobFunction(
            stdinData=None,
            executionName="Triggered by " + jobData.__dict__["PrivateExternalTrigger"]["type"]
        )
        return (False, None, None)

    #return vars = (failmessage, typeprivatevars, typepublicvars)
    def activate(self, jobguid, triggerType, jobObj, triggerOptions, salt, urlpasscode, nonurlpasscode):
        # Only ever called when the job has no trigger activated
        # by default nothing to do
        return (None, {}, {})

    def deactivate(self, jobguid, privateTriggerData):
        return
