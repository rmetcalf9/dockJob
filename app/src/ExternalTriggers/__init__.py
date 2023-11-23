import copy

from .ExternalTriggerTypes import getAllTriggerTypeInstances
from .api import register_api
from .privateApi import register_private_api
from encryption import getSafePasswordString, decryptPassword, encryptPassword, getSafeSaltString
import uuid

saltForJobIdPasswordEncryption="JDJiJDEyJFRGQmZ1RzhjY3IzVTVxTzVTeERXbnU="

class ExternalTriggerManager():
    safePasswordString = None
    appObj = None

    TriggerTypes = None
    def __init__(self, DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD, appObj):
        self.safePasswordString = getSafePasswordString(DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD)
        self.appObj = appObj
        self.TriggerTypes = getAllTriggerTypeInstances(self)

    def getStaticServerInfoData(self):
        types = {}
        for type in self.TriggerTypes:
            types[type] = self.TriggerTypes[type].getStaticServerInfoData()
        return {
            "types": types
        }

    def encodeJobGuid(self, job_guid):
        return encryptPassword(self.appObj.bcrypt, job_guid, saltForJobIdPasswordEncryption, self.safePasswordString)
    def decodeJobGuid(self, cypherText):
        #must use hardcoded salt as cannot use salts on the job as we don't know which job yet
        try:
            return decryptPassword(self.appObj.bcrypt, cypherText, saltForJobIdPasswordEncryption, self.safePasswordString)
        except:
            return None

    # 406 means message was received but there are no configured types to process
    def processTrigger(self, urlid, request_headers, request_data):
        possible_jobs_that_could_match = {}
        for type in self.TriggerTypes:
            jobGuid = self.decodeJobGuid(self.TriggerTypes[type].getEncodedJobGuidFromMessage(urlid, request_headers, request_data))
            if jobGuid is not None:
                if jobGuid not in possible_jobs_that_could_match.keys():
                    possible_jobs_that_could_match[jobGuid] = []
                possible_jobs_that_could_match[jobGuid].append(self.TriggerTypes[type])
        if len(possible_jobs_that_could_match) == 0:
            return {"result": "Fail"}, 406
        def dbfn(store_connection):
            return self.processTriggerWithContext(store_connection, possible_jobs_that_could_match, urlid, request_headers, request_data)
        return self.appObj.objectStore.executeInsideTransaction(dbfn)

    def processTriggerWithContext(self, store_connection, possible_jobs_that_could_match, urlid, request_headers, request_data):
        for jobGuid in possible_jobs_that_could_match.keys():
            jobData = self.appObj.appData['jobsData'].getJobRaw(jobGuid)
            if jobData is not None:
                PrivateExternalTrigger = jobData.__dict__["PrivateExternalTrigger"]
                if PrivateExternalTrigger["triggerActive"]:
                    (rawurlpasscode, rawnonurlpasscode) = self.getJobPasscodes(jobData)

                    for triggerType in possible_jobs_that_could_match[jobGuid]:
                        if jobData.__dict__["PrivateExternalTrigger"]["type"]==triggerType.__class__.__name__:
                            if triggerType.requestMatches(jobData, urlid, request_headers, request_data, rawurlpasscode, rawnonurlpasscode):
                                if jobData.__dict__["PrivateExternalTrigger"]["triggerActive"]:
                                    self.processMatchedTrigger(
                                        store_connection=store_connection,
                                        PrivateExternalTrigger=PrivateExternalTrigger,
                                        triggerType=triggerType,
                                        jobData=jobData,
                                        urlid=urlid,
                                        request_headers=request_headers,
                                        request_data=request_data,
                                        rawurlpasscode=rawurlpasscode,
                                        rawnonurlpasscode=rawnonurlpasscode
                                    )
                                    return {"result": "Success"}, 200

        return {"result": "Fail"}, 406

    def processMatchedTrigger(self, store_connection, PrivateExternalTrigger, triggerType, jobData, urlid, request_headers, request_data, rawurlpasscode,rawnonurlpasscode ):
        def submitJobFunction(stdinData, executionName="Triggered by " + PrivateExternalTrigger["type"]):
            self.appObj.jobExecutor.submitJobForExecution(
                jobGUID=jobData.guid,
                executionName=executionName,
                manual=False,
                stdinData=stdinData
            )

        (updateJobNeeded, typeprivatevars, typepublicvars) = triggerType.fireTrigger(
            submitJobFunction, jobData, urlid, request_headers, request_data, rawurlpasscode,rawnonurlpasscode
        )
        if updateJobNeeded:
            # This code is going to look something like
            PrivateExternalTrigger["typeprivatevars"] = typeprivatevars
            PrivateExternalTrigger["typepublicvars"] = typepublicvars
            jobData.setNewPrivateTriggerData(PrivateExternalTrigger)
            self.appObj.appData['jobsData']._saveJobToObjectStore(str(jobData.guid), store_connection)

    def getJobDictData(self, jobObj):
        if not jobObj.PrivateExternalTrigger["triggerActive"]:
            return { "triggerActive": False }
        (rawurlpasscode, rawnonurlpasscode) = self.getJobPasscodes(jobObj)

        return {
            "triggerActive": True,
            "type": jobObj.PrivateExternalTrigger["type"],
            "salt": jobObj.PrivateExternalTrigger["salt"],
            "urlpasscode": rawurlpasscode,
            "nonurlpasscode": rawnonurlpasscode,
            "encodedjobguid": self.encodeJobGuid(jobObj.__dict__["guid"]),
            "typepublicvars": jobObj.PrivateExternalTrigger["typepublicvars"]
        }

    def activateTrigger(self, jobguid, triggerType, triggerOptions):
        if triggerType not in self.TriggerTypes.keys():
            return {"result": "Fail", "message": "Invalid trigger type"}, 400
        def dbfn(store_connection):
            return self.activateTriggerWithStoreConnection(
                store_connection=store_connection,
                jobguid=jobguid,
                triggerType=triggerType,
                triggerTypeObj=self.TriggerTypes[triggerType],
                triggerOptions=triggerOptions
            )
        return self.appObj.objectStore.executeInsideTransaction(dbfn)

    def getJobPasscodes(self, jobObj):
        rawurlpasscode = decryptPassword(self.appObj.bcrypt, jobObj.PrivateExternalTrigger["urlpasscode"], jobObj.PrivateExternalTrigger["salt"], self.safePasswordString)
        rawnonurlpasscode = decryptPassword(self.appObj.bcrypt, jobObj.PrivateExternalTrigger["nonurlpasscode"], jobObj.PrivateExternalTrigger["salt"], self.safePasswordString)
        return (rawurlpasscode, rawnonurlpasscode)

    def activateTriggerWithStoreConnection(self, store_connection, jobguid, triggerType, triggerTypeObj, triggerOptions):
        jobObj = self.appObj.appData['jobsData'].getJobRaw(jobguid)
        if jobObj is None:
            return {"result": "Fail", "message": "Job not found"}, 404
        if jobObj.PrivateExternalTrigger["triggerActive"]:
            (rawurlpasscode, rawnonurlpasscode) = self.getJobPasscodes(jobObj)
            self.TriggerTypes[triggerType].deactivate(
                jobObj=jobObj,
                rawurlpasscode=rawurlpasscode,
                rawnonurlpasscode=rawnonurlpasscode
            )

        salt = getSafeSaltString(self.appObj.bcrypt)

        rawurlpasscode = str(uuid.uuid4())
        rawnonurlpasscode = str(uuid.uuid4())
        urlpasscode = encryptPassword(self.appObj.bcrypt, rawurlpasscode, salt, self.safePasswordString)
        nonurlpasscode = encryptPassword(self.appObj.bcrypt, rawnonurlpasscode, salt, self.safePasswordString)

        (failmessage, typeprivatevars, typepublicvars) = triggerTypeObj.activate(
            jobguid=jobObj.guid,
            triggerType=triggerType,
            jobObj=jobObj,
            triggerOptions=triggerOptions,
            salt=salt,
            rawurlpasscode=rawurlpasscode,
            rawnonurlpasscode=rawnonurlpasscode
        )
        if failmessage is not None:
            return {"result": "Fail", "message": failmessage}, 400

        privateTriggerData = {
            "triggerActive": True,
            "type": triggerType,
            "salt": salt,
            "urlpasscode": urlpasscode,
            "nonurlpasscode": nonurlpasscode,
            "typeprivatevars": typeprivatevars,
            "typepublicvars": typepublicvars
        }

        jobObj.setNewPrivateTriggerData(privateTriggerData)

        self.appObj.appData['jobsData']._saveJobToObjectStore(str(jobObj.guid), store_connection)

        return jobObj._caculatedDict(self.appObj), 201

    def deactivateTrigger(self, jobguid):
        def dbfn(store_connection):
            return self.deactivateTriggerWithStoreConnection(
                store_connection=store_connection,
                jobguid=jobguid
            )
        return self.appObj.objectStore.executeInsideTransaction(dbfn)

    def deactivateTriggerWithStoreConnection(self, store_connection, jobguid):
        jobObj = self.appObj.appData['jobsData'].getJobRaw(jobguid)
        if jobObj is None:
            return {"result": "Fail", "message": "Job not found"}, 404
        if not jobObj.PrivateExternalTrigger["triggerActive"]:
            return {"result": "Warning", "message": "Trigger was not active"}, 400

        triggerType = jobObj.__dict__["PrivateExternalTrigger"]["type"]
        if triggerType not in self.TriggerTypes:
            print("ERROR!!! - type in data not found when deactivating job" + jobObj.__dict__["PrivateExternalTrigger"]["type"] + " Trying to continue")
        else:
            (rawurlpasscode, rawnonurlpasscode) = self.getJobPasscodes(jobObj)
            self.TriggerTypes[triggerType].deactivate(
                jobObj=jobObj,
                rawurlpasscode=rawurlpasscode,
                rawnonurlpasscode=rawnonurlpasscode
            )

        privateTriggerData = {
            "triggerActive": False
        }

        jobObj.setNewPrivateTriggerData(privateTriggerData)
        self.appObj.appData['jobsData']._saveJobToObjectStore(str(jobObj.guid), store_connection)

        return jobObj._caculatedDict(self.appObj), 201

    def loopIterationForJob(self, jobObj, curTime):
        if not jobObj.PrivateExternalTrigger["triggerActive"]:
            return
        if jobObj.PrivateExternalTrigger["type"] not in self.TriggerTypes:
            raise Exception("Invalid trigger type")
        triggerType = self.TriggerTypes[jobObj.PrivateExternalTrigger["type"]]
        (updateJobNeeded, typeprivatevars, typepublicvars, newrawurlpasscode, newrawnonurlpasscode) = triggerType.loopIterationForJob(
            jobObj=jobObj,
            curTime=curTime,
            getJobPasscodes=self.getJobPasscodes
        )
        if updateJobNeeded:
            print("DEBUG TODO DEL", "Saving updated trigger data")
            PrivateExternalTrigger = copy.deepcopy(jobObj.PrivateExternalTrigger)
            PrivateExternalTrigger["typeprivatevars"] = typeprivatevars
            PrivateExternalTrigger["typepublicvars"] = typepublicvars

            if newrawurlpasscode is not None:
                salt = getSafeSaltString(self.appObj.bcrypt)
                encrypted = encryptPassword(self.appObj.bcrypt, newrawurlpasscode, salt, self.safePasswordString)
                PrivateExternalTrigger["urlpasscode"] = encrypted

            if newrawnonurlpasscode is not None:
                salt = getSafeSaltString(self.appObj.bcrypt)
                encrypted = encryptPassword(self.appObj.bcrypt, newrawnonurlpasscode, salt, self.safePasswordString)
                PrivateExternalTrigger["nonurlpasscode"] = encrypted

            jobObj.setNewPrivateTriggerData(PrivateExternalTrigger)

            print("DEBUG TODO DEL", PrivateExternalTrigger)
            print("DEBUG TODO DEL - testing decrypt of new codes works")
            (_, _) = self.getJobPasscodes(jobObj)
            print("DEBUG TODO DEL - complete")

            def dbfn(store_connection):
                self.appObj.appData['jobsData']._saveJobToObjectStore(str(jobObj.guid), store_connection)
            self.appObj.objectStore.executeInsideTransaction(dbfn)
