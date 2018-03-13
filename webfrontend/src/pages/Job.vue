<template>
  <div>
    <q-list highlight>
      <q-item><q-item-main >
          <q-item-tile label>Job Name</q-item-tile>
          <q-item-tile sublabel>{{ jobData.name }}</q-item-tile>
      </q-item-main></q-item>
      <q-item><q-item-main >
          <q-item-tile label>GUID</q-item-tile>
          <q-item-tile sublabel>{{ jobData.guid }}</q-item-tile>
      </q-item-main></q-item>
      <q-item><q-item-main >
          <q-item-tile label>Command</q-item-tile>
          <q-item-tile sublabel>{{ jobData.command }}</q-item-tile>
      </q-item-main></q-item>
      <q-item><q-item-main >
          <q-item-tile label>Scheduled Running Enabled</q-item-tile>
          <q-item-tile sublabel>{{ jobData.enabled }}</q-item-tile>
      </q-item-main></q-item>
      <q-item><q-item-main >
          <q-item-tile label>Repetition Interval</q-item-tile>
          <q-item-tile sublabel>{{ jobData.repetitionInterval }}</q-item-tile>
      </q-item-main></q-item>
      <q-item><q-item-main >
          <q-item-tile label>Next Scheduled Run</q-item-tile>
          <q-item-tile sublabel>{{ jobData.nextScheduledRun }}</q-item-tile>
      </q-item-main></q-item>
      <q-item><q-item-main >
          <q-item-tile label>Creation Date</q-item-tile>
          <q-item-tile sublabel>{{ jobData.creationDate }}</q-item-tile>
      </q-item-main></q-item>
      <q-item><q-item-main >
          <q-item-tile label>Last Update Date</q-item-tile>
          <q-item-tile sublabel>{{ jobData.lastUpdateDate }}</q-item-tile>
      </q-item-main></q-item>
      <q-item><q-item-main >
          <q-item-tile label>Last Run Date</q-item-tile>
          <q-item-tile sublabel>{{ jobData.lastRunDate }}</q-item-tile>
      </q-item-main></q-item>
      <q-item><q-item-main >
          <q-item-tile label>Executions</q-item-tile>
          <q-item-tile sublabel>
            <q-table
              title='Executions'
              :data="jobExecutionData"
              :columns="jobTableColumns"
              :visible-columns="visibleColumns"
              :filter="filter"
              row-key="name"
              :pagination.sync="serverPagination"
              :loading="loading"
              @request="requestExecutionData"
            >
              <template slot="top-right" slot-scope="props">
              <q-table-columns
                color="secondary"
                class="q-mr-sm"
                v-model="visibleColumns"
                :columns="jobTableColumns"
              />
              <q-search clearable hide-underline v-model="filter" />
              </template>
            </q-table>
    </q-item-tile>
      </q-item-main></q-item>
    </q-list>
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
  </div>

</template>

<script>
import { Notify } from 'quasar'
import globalStore from '../store/globalStore'
import callbackHelper from '../callbackHelper'

export default {
  data () {
    return {
      createJobModalDialog: {},
      jobTableColumns: [
        // { name: 'guid', required: false, label: 'GUID', align: 'left', field: 'guid', sortable: false, filter: true },
        { name: 'executionName', required: false, label: 'Name', align: 'left', field: 'executionName', sortable: false, filter: true },
        { name: 'stage', required: false, label: 'Stage', align: 'left', field: 'stage', sortable: false, filter: true },
        { name: 'resultReturnCode', required: false, label: 'Return Code', align: 'left', field: 'resultReturnCode', sortable: false, filter: true },
        { name: 'manual', required: false, label: 'Manual Run', align: 'left', field: 'manual', sortable: false, filter: true },
        { name: 'dateCreated', required: false, label: 'Creation Date', align: 'left', field: 'dateCreated', sortable: false, filter: true },
        { name: 'dateStarted', required: false, label: 'Start Date', align: 'left', field: 'dateStarted', sortable: false, filter: true },
        { name: 'dateCompleted', required: false, label: 'Completion Date', align: 'left', field: 'dateCompleted', sortable: false, filter: true },
        { name: 'resultSTDOUT', required: false, label: 'Output', align: 'left', field: 'resultSTDOUT', sortable: false, filter: true },
        { name: 'jobGUID', required: false, label: 'Last Job GUID', align: 'left', field: 'jobGUID', sortable: false, filter: true },
        { name: 'jobCommand', required: false, label: 'Job Command', align: 'left', field: 'jobCommand', sortable: false, filter: true }
      ],
      jobExecutionData: [],
      filter: '',
      loading: false,
      serverPagination: {
        page: 1,
        rowsNumber: 10 // specifying this determines pagination is server-side
      },
      visibleColumns: ['executionName', 'stage', 'resultReturnCode'],
      jobData: {}
    }
  },
  methods: {
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
          TTT.jobData = response.data
          globalStore.commit('SET_PAGE_TITLE', 'Job ' + TTT.jobData.name)
        },
        error: function (error) {
          Notify.create('Job query failed - ' + callbackHelper.getErrorFromResponse(error))
          this.jobData = {}
        }
      }
      globalStore.getters.apiFN('GET', 'jobs/' + this.$route.params.jobGUID, undefined, callback)
      this.requestExecutionData({
        pagination: this.serverPagination,
        filter: this.filter
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
          TTT.serverPagination = pagination

          // we also set (or update) rowsNumber
          TTT.serverPagination.rowsNumber = response.data.pagination.total

          // then we update the rows with the fetched ones
          TTT.jobExecutionData = response.data.result

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
      var queryString = 'jobs/' + this.$route.params.jobGUID + '/execution?pagesize=' + pagination.rowsPerPage.toString() + '&offset=' + (pagination.rowsPerPage * (pagination.page - 1)).toString()
      if (filter !== '') {
        queryString = 'jobs/' + this.$route.params.jobGUID + '/execution?pagesize=' + pagination.rowsPerPage.toString() + '&query=' + filter + '&offset=' + (pagination.rowsPerPage * (pagination.page - 1)).toString()
      }
      globalStore.getters.apiFN('GET', queryString, undefined, callback)
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
