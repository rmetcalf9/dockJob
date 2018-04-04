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
      <q-item><q-item-main >
          <q-item-tile label>Last Run Date</q-item-tile>
          <q-item-tile sublabel v-if="everRun(jobData)">{{ jobData.lastRunDateString }}</q-item-tile>
          <q-item-tile sublabel v-if="!everRun(jobData)">Never run</q-item-tile>
      </q-item-main></q-item>
      <q-item v-if="everRun(jobData)"><q-item-main >
          <q-item-tile label>Last Run Return Code</q-item-tile>
          <q-item-tile sublabel>{{ jobData.lastRunReturnCode }}</q-item-tile>
      </q-item-main></q-item>
      <q-item v-if="everRun(jobData)"><q-item-main >
          <q-item-tile label>Last Execution GUID</q-item-tile>
          <q-item-tile sublabel>{{ jobData.lastRunExecutionGUID }}</q-item-tile>
      </q-item-main></q-item>
    </q-list>
    <q-table
      title='Executions'
      :data="jobExecutionData"
      :columns="jobTableColumns"
      :visible-columns="jobExecutionsDataTableSettings.visibleColumns"
      :filter="jobExecutionsDataTableSettings.filter"
      row-key="name"
      :pagination.sync="jobExecutionsDataTableSettings.serverPagination"
      :loading="loading"
      @request="requestExecutionData"
      :rows-per-page-options="rowsPerPageOptions"
    >
      <template slot="top-right" slot-scope="props">
        <q-table-columns
          color="secondary"
          class="q-mr-sm"
          v-model="jobExecutionsDataTableSettings.visibleColumns"
          :columns="jobTableColumns"
        />
        <q-search clearable hide-underline v-model="jobExecutionsDataTableSettings.filter" />
      </template>
      <q-td slot="body-cell-resultSTDOUT" slot-scope="props" :props="props">
        <STDOutput :val="props.value" />
      </q-td>
      <q-td slot="body-cell-jobCommand" slot-scope="props" :props="props">
        <div v-for="curVal in getLineArray(props.value)" :key=curVal.p>{{ curVal.v }}</div>
      </q-td>

    </q-table>
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
import dataTableSettings from '../store/dataTableSettings'
import callbackHelper from '../callbackHelper'
import STDOutput from '../components/STDOutput'
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
    STDOutput
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
      jobTableColumns: [
        { name: 'guid', required: false, label: 'Execution GUID', align: 'left', field: 'guid', sortable: false, filter: true },
        { name: 'executionName', required: false, label: 'Name', align: 'left', field: 'executionName', sortable: false, filter: true },
        { name: 'stage', required: false, label: 'Stage', align: 'left', field: 'stage', sortable: false, filter: true },
        { name: 'resultReturnCode', required: false, label: 'Return Code', align: 'left', field: 'resultReturnCode', sortable: false, filter: true },
        { name: 'manual', required: false, label: 'Manual Run', align: 'left', field: 'manual', sortable: false, filter: true },
        { name: 'dateCreated', required: false, label: 'Creation Date', align: 'left', field: 'dateCreatedString', sortable: false, filter: true },
        { name: 'dateStarted', required: false, label: 'Start Date', align: 'left', field: 'dateStartedString', sortable: false, filter: true },
        { name: 'dateCompleted', required: false, label: 'Completion Date', align: 'left', field: 'dateCompletedString', sortable: false, filter: true },
        { name: 'resultSTDOUT', required: false, label: 'Output', align: 'left', field: 'resultSTDOUT', sortable: false, filter: true },
        { name: 'jobGUID', required: false, label: 'Job GUID', align: 'left', field: 'jobGUID', sortable: false, filter: true },
        { name: 'jobCommand', required: false, label: 'Job Command', align: 'left', field: 'jobCommand', sortable: false, filter: true }
      ],
      jobExecutionData: [],
      loading: false,
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
          Notify.create('Job Execution Request Sent')
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
      this.requestExecutionData({
        pagination: this.jobExecutionsDataTableSettings.serverPagination,
        filter: this.jobExecutionsDataTableSettings.filter
      })
    },
    requestExecutionData ({ pagination, filter }) {
      var TTT = this
      TTT.loading = true
      var callback = {
        ok: function (response) {
          // console.log(response.data.guid)
          TTT.loading = false

          // updating pagination to reflect in the UI
          TTT.jobExecutionsDataTableSettings.serverPagination = pagination
          // we also set (or update) rowsNumber
          TTT.jobExecutionsDataTableSettings.serverPagination.rowsNumber = response.data.pagination.total
          TTT.jobExecutionsDataTableSettings.serverPagination.filter = filter
          TTT.jobExecutionsDataTableSettings.serverPagination.rowsPerPage = response.data.pagination.pagesize

          // then we update the rows with the fetched ones
          TTT.jobExecutionData = response.data.result
          TTT.jobExecutionData.map(function (obj) {
            obj.dateCreatedString = userSettings.getters.userTimeStringFN(obj.dateCreated)
            obj.dateStartedString = userSettings.getters.userTimeStringFN(obj.dateStarted)
            obj.dateCompletedString = userSettings.getters.userTimeStringFN(obj.dateCompleted)
            return obj
          })

          // finally we tell QTable to exit the "loading" state
          TTT.loading = false
        },
        error: function (error) {
          TTT.loading = false
          Notify.create('Job query failed - ' + callbackHelper.getErrorFromResponse(error))
        }
      }
      if (pagination.page === 0) {
        pagination.page = 1
      }

      var queryString = ''
      if (pagination.rowsPerPage === 0) {
        queryString = 'jobs/' + this.$route.params.jobGUID + '/execution'
        if (filter !== '') {
          queryString = 'jobs/' + this.$route.params.jobGUID + '/execution?query=' + filter
        }
      } else {
        queryString = 'jobs/' + this.$route.params.jobGUID + '/execution?pagesize=' + pagination.rowsPerPage.toString() + '&offset=' + (pagination.rowsPerPage * (pagination.page - 1)).toString()
        if (filter !== '') {
          queryString = 'jobs/' + this.$route.params.jobGUID + '/execution?pagesize=' + pagination.rowsPerPage.toString() + '&query=' + filter + '&offset=' + (pagination.rowsPerPage * (pagination.page - 1)).toString()
        }
      }
      // console.log(queryString)
      globalStore.getters.apiFN('GET', queryString, undefined, callback)
    }
  },
  computed: {
    datastoreState () {
      return globalStore.getters.datastoreState
    },
    jobExecutionsDataTableSettings () {
      return dataTableSettings.getters.jobExecutions
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
