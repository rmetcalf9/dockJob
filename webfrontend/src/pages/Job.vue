<template>
  <div>
    <q-list >
      <q-item highlight @click.native="openEditJobModalDialog">
        <q-item-main >
          <q-item-tile label>Job {{ jobData.name }}</q-item-tile>
          <q-item-tile sublabel>{{ jobData.guid }}</q-item-tile>
        </q-item-main>
        <q-item-side right icon="mode_edit" />
      </q-item>
      <q-item><q-item-main >
          <q-item-tile label>Command</q-item-tile>
          <q-item-tile sublabel><div v-for="curVal in getLineArray(jobData.command)" :key=curVal.p>{{ curVal.v }}</div></q-item-tile>
      </q-item-main></q-item>
      <q-item>
        <q-item-main >
          <q-item-tile label>Repetition Interval</q-item-tile>
          <q-item-tile sublabel v-if="jobData.enabled">{{ jobData.repetitionInterval }}</q-item-tile>
          <q-item-tile sublabel v-if="!jobData.enabled">Automatic running disabled</q-item-tile>
        </q-item-main>
      </q-item>
      <q-item v-if="jobData.enabled"><q-item-main >
          <q-item-tile label>Next Scheduled Run</q-item-tile>
          <q-item-tile sublabel>{{ jobData.nextScheduledRunString }}</q-item-tile>
      </q-item-main></q-item>
      <q-item><q-item-main >
          <q-item-tile label>Creation Date</q-item-tile>
          <q-item-tile sublabel>{{ jobData.creationDateString }}</q-item-tile>
      </q-item-main></q-item>
      <q-item><q-item-main >
          <q-item-tile label>Last Update Date</q-item-tile>
          <q-item-tile sublabel>{{ jobData.lastUpdateDateString }}</q-item-tile>
      </q-item-main></q-item>
      <q-item v-if="jobData.mostRecentCompletionStatus === 'Success'"><q-item-main >
          <q-item-tile label class="bg-positive text-white">Last Run Date</q-item-tile>
          <q-item-tile sublabel v-if="everRun(jobData)">{{ jobData.lastRunDateString }}</q-item-tile>
          <q-item-tile sublabel v-if="!everRun(jobData)">Never run</q-item-tile>
      </q-item-main></q-item>
      <q-item v-if="jobData.mostRecentCompletionStatus === 'Fail'"><q-item-main >
          <q-item-tile label class="bg-negative text-white">Last Run Date</q-item-tile>
          <q-item-tile sublabel v-if="everRun(jobData)">{{ jobData.lastRunDateString }}</q-item-tile>
          <q-item-tile sublabel v-if="!everRun(jobData)">Never run</q-item-tile>
      </q-item-main></q-item>
      <q-item v-if="jobData.mostRecentCompletionStatus === 'Unknown'"><q-item-main >
          <q-item-tile label class="bg-primary text-white">Last Run Date</q-item-tile>
          <q-item-tile sublabel v-if="everRun(jobData)">{{ jobData.lastRunDateString }}</q-item-tile>
          <q-item-tile sublabel v-if="!everRun(jobData)">Never run</q-item-tile>
      </q-item-main></q-item>
      <div v-if="everRun(jobData)">
        <q-item><q-item-main >
            <q-item-tile label>Last Run Return Code</q-item-tile>
            <q-item-tile sublabel>{{ jobData.lastRunReturnCode }}</q-item-tile>
        </q-item-main></q-item>
        <q-item><q-item-main >
            <q-item-tile label>Last Execution GUID</q-item-tile>
            <q-item-tile sublabel>{{ jobData.lastRunExecutionGUID }}</q-item-tile>
        </q-item-main></q-item>
      </div>
    </q-list>
    <ExecutionTable
      ref="ExecutionTable"
      title="Executions Table"
      DataTableSettingsPrefix='jobExecutions'
      :apiPath="'jobs/' + this.$route.params.jobGUID + '/execution'"
    >
    </ExecutionTable>
    <q-btn
      color="primary"
      push
      @click="refreshJobData"
    >Refresh</q-btn>
    <q-btn
      color="primary"
      push
      @click="runnow"
    >Run Now</q-btn>
    <CreateJobModal
      ref="createJobModalDialog"
      v-model="createJobModalDialog"
    />
  </div>
</template>

<script>
import { Notify } from 'quasar'
import globalStore from '../store/globalStore'
import callbackHelper from '../callbackHelper'
import ExecutionTable from '../components/ExecutionTable'
import CreateJobModal from '../components/CreateJobModal'
import userSettings from '../store/userSettings'

function addDateStringsToJobData (obj) {
  obj.creationDateString = userSettings.getters.userTimeStringFN(obj.creationDate)
  obj.nextScheduledRunString = userSettings.getters.userTimeStringFN(obj.nextScheduledRun)
  obj.lastUpdateDateString = userSettings.getters.userTimeStringFN(obj.lastUpdateDate)
  obj.lastRunDateString = userSettings.getters.userTimeStringFN(obj.lastRunDate)
  return obj
}

export default {
  components: {
    CreateJobModal,
    ExecutionTable
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
      promptTextValue: ''
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
          Notify.create({color: 'positive', detail: 'Job Execution Request Sent'})
          // this.refreshJobData() No point doing this immediately
        },
        error: function (error) {
          Notify.create('Request for execution failed - ' + callbackHelper.getErrorFromResponse(error))
        }
      }
      this.$q.dialog({
        title: 'Submit request to run ' + TTT.jobData.name,
        message: 'User name for execution',
        prompt: {
          model: '',
          type: 'text' // optional
        },
        cancel: true,
        color: 'secondary'
      }).then(data => {
        var params = {name: data}
        globalStore.getters.apiFN('POST', 'jobs/' + TTT.$route.params.jobGUID + '/execution', params, callback)
      })
    },
    refreshJobData () {
      var TTT = this
      var callback = {
        ok: function (response) {
          TTT.jobData = addDateStringsToJobData(response.data)
          globalStore.commit('SET_PAGE_TITLE', 'Job ' + TTT.jobData.name)
        },
        error: function (error) {
          Notify.create('Job query failed - ' + callbackHelper.getErrorFromResponse(error))
          this.jobData = {}
        }
      }
      globalStore.getters.apiFN('GET', 'jobs/' + this.$route.params.jobGUID, undefined, callback)
      this.$refs.ExecutionTable.refreshData()
    }
  },
  computed: {
    datastoreState () {
      return globalStore.getters.datastoreState
    }
  },
  mounted () {
    // once mounted, we need to trigger the initial server data fetch
    globalStore.commit('SET_PAGE_TITLE', 'Job ' + this.$route.params.jobGUID)
    this.refreshJobData()
  }
}
</script>

<style>
</style>
