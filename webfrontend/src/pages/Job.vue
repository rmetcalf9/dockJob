<template>
  <div>
    <q-list >
      <q-item clickable v-ripple highlight @click.native="openEditJobModalDialog">
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
      <q-item v-if="typeof(jobData.StateChangeSuccessJobGUID) !== 'undefined' && jobData.StateChangeSuccessJobGUID !== null"><q-item-section >
          <q-item-label>State Change Success Job: {{ jobData.StateChangeSuccessJobNAME }}</q-item-label>
          <q-item-label caption>
            <router-link :to="'/jobs/' + jobData.StateChangeSuccessJobGUID" tag="a" class="text-grey-8">
              {{ jobData.StateChangeSuccessJobGUID }}
            </router-link>
          </q-item-label>
      </q-item-section></q-item>
      <q-item v-if="typeof(jobData.StateChangeFailJobGUID) !== 'undefined' && jobData.StateChangeFailJobGUID !== null"><q-item-section >
          <q-item-label>State Change Fail Job: {{ jobData.StateChangeFailJobNAME }}</q-item-label>
          <q-item-label caption>
            <router-link :to="'/jobs/' + jobData.StateChangeFailJobGUID" tag="a" class="text-grey-8">
              {{ jobData.StateChangeFailJobGUID }}
            </router-link>
          </q-item-label>
      </q-item-section></q-item>
      <q-item v-if="typeof(jobData.StateChangeUnknownJobGUID) !== 'undefined' && jobData.StateChangeUnknownJobGUID !== null"><q-item-section >
          <q-item-label>State Change Unknown Job: {{ jobData.StateChangeUnknownJobNAME }}</q-item-label>
          <q-item-label caption>
            <router-link :to="'/jobs/' + jobData.StateChangeUnknownJobGUID" tag="a" class="text-grey-8">
              {{ jobData.StateChangeUnknownJobGUID }}
            </router-link>
          </q-item-label>
      </q-item-section></q-item>
      <q-item v-if="typeof(jobData.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown) !== 'undefined' && jobData.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown !== null"><q-item-section >
          <q-item-label>Minutes before setting completion status to Unknown</q-item-label>
          <q-item-label caption>{{ jobData.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown }}</q-item-label>
      </q-item-section></q-item>
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
          Notify.create({color: 'positive', detail: 'Job Execution Request Sent'})
          // this.refreshJobData() No point doing this immediately
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
      }).then(data => {
        var params = {name: data}
        globalStore.getters.apiFN('POST', 'jobs/' + TTT.$route.params.jobGUID + '/execution', params, callback)
      })
    },
    refreshJobData () {
      this.loadedJobGUID = this.$route.params.jobGUID
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
