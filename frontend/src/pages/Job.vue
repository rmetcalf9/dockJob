<template>
  <div>
    <q-list >
      <q-item clickable v-ripple highlight @click="openEditJobModalDialog">
        <q-item-section >
          <q-item-label>Job {{ jobData.name }}</q-item-label>
          <q-item-label caption>{{ jobData.guid }}</q-item-label>
        </q-item-section>
        <q-item-section avatar>
          <q-icon color="primary" name="mode_edit" />
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section >
          <q-item-label>Command</q-item-label>
          <q-item-label caption><div v-for="curVal in getLineArray(jobData.command)" :key=curVal.p>{{ curVal.v }}</div></q-item-label>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section >
          <q-item-label>Repetition Interval</q-item-label>
          <q-item-label caption v-if="jobData.enabled">{{ jobData.repetitionInterval }}</q-item-label>
          <q-item-label caption v-if="!jobData.enabled">Automatic running disabled</q-item-label>
        </q-item-section>
      </q-item>
      <q-item v-if="jobData.enabled"><q-item-section >
          <q-item-label>Next Scheduled Run</q-item-label>
          <q-item-label caption>{{ jobData.nextScheduledRunString }}</q-item-label>
      </q-item-section></q-item>
      <q-item><q-item-section >
          <q-item-label>Creation Date</q-item-label>
          <q-item-label caption>{{ jobData.creationDateString }}</q-item-label>
      </q-item-section></q-item>
      <q-item><q-item-section >
          <q-item-label>Last Update Date</q-item-label>
          <q-item-label caption>{{ jobData.lastUpdateDateString }}</q-item-label>
      </q-item-section></q-item>
      <q-item v-if="jobData.mostRecentCompletionStatus === 'Success'"><q-item-section >
          <q-item-label class="bg-positive text-white">Last Run Date</q-item-label>
          <q-item-label caption v-if="everRun(jobData)">{{ jobData.lastRunDateString }}</q-item-label>
          <q-item-label caption v-if="!everRun(jobData)">Never run</q-item-label>
      </q-item-section></q-item>
      <q-item v-if="jobData.mostRecentCompletionStatus === 'Fail'"><q-item-section >
          <q-item-label class="bg-negative text-white">Last Run Date</q-item-label>
          <q-item-label caption v-if="everRun(jobData)">{{ jobData.lastRunDateString }}</q-item-label>
          <q-item-label caption v-if="!everRun(jobData)">Never run</q-item-label>
      </q-item-section></q-item>
      <q-item v-if="jobData.mostRecentCompletionStatus === 'Unknown'"><q-item-section >
          <q-item-label class="bg-primary text-white">Last Run Date</q-item-label>
          <q-item-label caption v-if="everRun(jobData)">{{ jobData.lastRunDateString }}</q-item-label>
          <q-item-label caption v-if="!everRun(jobData)">Never run</q-item-label>
      </q-item-section></q-item>
      <div v-if="everRun(jobData)">
        <q-item><q-item-section >
            <q-item-label>Last Run Return Code</q-item-label>
            <q-item-label caption>{{ jobData.lastRunReturnCode }}</q-item-label>
        </q-item-section></q-item>
        <q-item><q-item-section >
            <q-item-label>Last Execution GUID</q-item-label>
            <q-item-label caption>{{ jobData.lastRunExecutionGUID }}</q-item-label>
        </q-item-section></q-item>
      </div>
      <q-item><q-item-section >
          <q-item-label>Pinned</q-item-label>
          <q-item-label caption>{{ jobData.pinned }}</q-item-label>
      </q-item-section></q-item>
      <div v-for="stateChangeJobObj in stateChangeJobObjs" :key=stateChangeJobObj.id>
        <q-item v-if="typeof(jobData[stateChangeJobObj.guidFieldName]) !== 'undefined' && jobData[stateChangeJobObj.guidFieldName] !== null"><q-item-section >
            <q-item-label>Post completion {{ stateChangeJobObj.text }} Job: {{ jobData[stateChangeJobObj.nameFieldName] }}</q-item-label>
            <q-item-label caption>
              <router-link :to="'/jobs/' + jobData[stateChangeJobObj.guidFieldName]" class="text-grey-8">
                {{ jobData[stateChangeJobObj.guidFieldName] }}
              </router-link>
            </q-item-label>
        </q-item-section></q-item>
      </div>
      <q-item v-if="typeof(jobData.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown) !== 'undefined' && jobData.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown !== null"><q-item-section >
          <q-item-label>Minutes before setting completion status to Unknown</q-item-label>
          <q-item-label caption>{{ jobData.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown }}</q-item-label>
      </q-item-section></q-item>
    </q-list>
    <ExecutionTable
      ref="ExecutionTable"
      title="Executions Table"
      DataTableSettingsPrefix='jobExecutions'
      :apiPath="'/jobs/' + this.$route.params.jobGUID + '/execution'"
    >
    </ExecutionTable>
    <table><tr><td>
      <q-btn
        color="primary"
        push
        @click="refreshJobData"
      >Refresh</q-btn>
    </td><td>
      <q-btn
        color="primary"
        push
        @click="runnow"
      >Run Now</q-btn>
    </td></tr></table>
    <CreateJobModal
      ref="createJobModalDialog"
    />
  </div>
</template>

<script>
import { Notify } from 'quasar'
import callbackHelper from '../callbackHelper'
import ExecutionTable from '../components/ExecutionTable.vue'
import CreateJobModal from '../components/CreateJobModal.vue'
import globalUtils from '../globalUtils'
import callDockjobBackendApi from '../callDockjobBackendApi'
import { useLoginStateStore } from 'stores/loginState'
import { useServerStaticStateStore } from 'stores/serverStaticState'
import miscFns from '../miscFns'


function addDateStringsToJobData (obj) {
  obj.creationDateString = miscFns.timeString(obj.creationDate)
  obj.nextScheduledRunString = miscFns.timeString(obj.nextScheduledRun)
  obj.lastUpdateDateString = miscFns.timeString(obj.lastUpdateDate)
  obj.lastRunDateString = miscFns.timeString(obj.lastRunDate)
  return obj
}

export default {
  name: 'App-Job',
  components: {
    CreateJobModal,
    ExecutionTable
  },
  setup () {
    const loginStateStore = useLoginStateStore()
    const serverStaticStateStore = useServerStaticStateStore()
    return { loginStateStore, serverStaticStateStore }
  },
  data () {
    return {
      rowsPerPageOptions: [5, 10, 25, 50, 100, 200],
      everRun: function (item) {
        if (typeof (item.lastRunDate) === 'undefined') {
          return false
        }
        return (item.lastRunDate !== null)
      },
      getLineArray: function (str) {
        if (typeof (str) === 'undefined') return undefined
        var c = 0
        return str.split('\n').map(function (v) { return { p: ++c, v: v } })
      },
      createJobModalDialog: {},
      jobData: {},
      promptTextValue: '',
      loadedJobGUID: ''
    }
  },
  methods: {
    openEditJobModalDialog () {
      var child = this.$refs.createJobModalDialog
      var TTTT = this
      child.openCreateJobDialog(function (newJob) {
        TTTT.jobData = addDateStringsToJobData(newJob)
      }, TTTT.jobData)
    },
    runnow () {
      var TTT = this
      if (typeof (this.jobData.name) === 'undefined') {
        Notify.create('Error job data not loaded')
        return
      }
      var callback = {
        ok: function (response) {
          Notify.create({color: 'positive', message: 'Job Execution Request Sent'})
          setTimeout(() => {
            TTT.refreshJobData()
          }, "300");
        },
        error: function (error) {
          Notify.create('Request for execution failed - ' + callbackHelper.getErrorFromResponse(error))
        }
      }
      this.$q.dialog({
        title: 'Submit request to run ' + TTT.jobData.name,
        message: 'Name for execution',
        prompt: {
          model: '',
          type: 'text' // optional
        },
        cancel: true,
        color: 'secondary'
      }).onOk(data => {
        var params = {name: data}

        const wrappedCallApiFn = callDockjobBackendApi.getWrappedCallApi({
          loginStateStore: TTT.loginStateStore,
          apiurl: TTT.serverStaticStateStore.staticServerInfo.data.apiurl
        })
        wrappedCallApiFn({
          method: 'POST',
          path: '/jobs/' + TTT.$route.params.jobGUID + '/execution',
          postdata: params,
          callback: callback
        })
      })
    },
    refreshJobData () {
      this.loadedJobGUID = this.$route.params.jobGUID
      var TTT = this
      var callback = {
        ok: function (response) {
          TTT.jobData = addDateStringsToJobData(response.data)
        },
        error: function (error) {
          Notify.create('Job query failed - ' + callbackHelper.getErrorFromResponse(error))
          this.jobData = {}
        }
      }
      const wrappedCallApiFn = callDockjobBackendApi.getWrappedCallApi({
        loginStateStore: TTT.loginStateStore,
        apiurl: TTT.serverStaticStateStore.staticServerInfo.data.apiurl
      })
      wrappedCallApiFn({
        method: 'GET',
        path: '/jobs/' + this.$route.params.jobGUID,
        postdata: undefined,
        callback: callback
      })
      this.$refs.ExecutionTable.refreshData()
    }
  },
  computed: {
    stateChangeJobObjs () {
      return globalUtils.getPostCompletionJobTypeList()
    }
  },
  mounted () {
    // once mounted, we need to trigger the initial server data fetch
    this.refreshJobData()
  },
  updated () {
    // Required as when the page is updated to the same page vue will reuse the compoennt and not reload the data
    // This event is also called very often and when we jump away from the page so it needs to limited be
    if (typeof (this.$route.params.jobGUID) === 'undefined') {
      return
    }
    if (this.loadedJobGUID === this.$route.params.jobGUID) {
      return
    }
    this.refreshJobData()
  }
}
</script>

<style>
</style>
