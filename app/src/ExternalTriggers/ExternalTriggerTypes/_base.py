
class externalTriggerBaseClass():
    externalTriggerManager = None
    typeName = None
    def __init__(self, externalTriggerManager, typeName):
        self.externalTriggerManager = externalTriggerManager
        self.typeName = typeName

    # Trigger types can have an endpoint this is for things like getting auth codes from google
    def getTypeName(self):
        return self.typeName

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
    def activate(self, jobguid, triggerType, jobObj, triggerOptions, salt, rawurlpasscode, rawnonurlpasscode):
        # Only ever called when the job has no trigger activated
        # by default nothing to do
        return (None, {}, {})

    def deactivate(self, jobObj, rawurlpasscode, rawnonurlpasscode):
        return

    # Return value (updateJobNeeded, typeprivatevars, typepublicvars, newrawurlpasscode, newrawnonurlpasscode)
    def loopIterationForJob(self, jobObj, curTime, getJobPasscodes):
        #int(datetime.datetime.now().timestamp() * 1000)
        return (False, None, None, None, None)