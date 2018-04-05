<template>
  <div>
    <q-table
      title='Jobs'
      :data="jobData"
      :columns="jobTableColumns"
      :visible-columns="jobsDataTableSettings.visibleColumns"
      :filter="jobsDataTableSettings.filter"
      row-key="name"
      :pagination.sync="jobsDataTableSettings.serverPagination"
      :loading="loading"
      @request="request"
      selection="single"
      :selected.sync="selectedSecond"
      :rows-per-page-options="rowsPerPageOptions"
    >
      <template slot="top-selection" slot-scope="props">
        <q-btn flat round delete icon="delete" @click="deleteJob" />
      </template>

      <template slot="top-left" slot-scope="props">
        <q-btn
          color="primary"
          push
          @click="openCreateJobModalDialog"
        >Create Job</q-btn>
      </template>
      <template slot="top-right" slot-scope="props">
      <q-table-columns
        color="secondary"
        class="q-mr-sm"
        v-model="jobsDataTableSettings.visibleColumns"
        :columns="jobTableColumns"
      />
      <q-search clearable hide-underline v-model="jobsDataTableSettings.filter" />
      </template>

      <q-td slot="body-cell-..." slot-scope="props" :props="props">
        <q-btn flat color="primary" icon="keyboard_arrow_right" label="" @click="$router.push('/jobs/' + props.row.guid)" />
      </q-td>
      <q-td slot="body-cell-command" slot-scope="props" :props="props">
        <div v-for="curVal in getLineArray(props.value)" :key=curVal.p>{{ curVal.v }}</div>
      </q-td>

    </q-table>
    <CreateJobModal
      ref="createJobModalDialog"
      v-model="createJobModalDialog"
    />
  </div>

</template>

<script>
import { Notify, Dialog } from 'quasar'
import globalStore from '../store/globalStore'
import dataTableSettings from '../store/dataTableSettings'
import CreateJobModal from '../components/CreateJobModal'
import callbackHelper from '../callbackHelper'
import userSettings from '../store/userSettings'
import restcallutils from '../restcallutils'

export default {
  components: {
    CreateJobModal
  },
  data () {
    return {
      rowsPerPageOptions: [5, 10, 25, 50, 100, 200],
      getLineArray: function (str) {
        if (typeof (str) === 'undefined') return undefined
        var c = 0
        return str.split('\n').map(function (v) { return { p: ++c, v: v } })
      },
      createJobModalDialog: {},
      jobTableColumns: [
        // { name: 'guid', required: false, label: 'GUID', align: 'left', field: 'guid', sortable: false, filter: true },
        { name: 'name', required: true, label: 'Job Name', align: 'left', field: 'name', sortable: true, filter: true },
        { name: 'enabled', required: false, label: 'Scheduled Running Enabled', align: 'left', field: 'enabled', sortable: true, filter: true },
        { name: 'creationDate', required: false, label: 'Created', align: 'left', field: 'creationDateString', sortable: true, filter: true },
        { name: 'lastRunDate', required: false, label: 'Last Run', align: 'left', field: 'lastRunDateString', sortable: true, filter: true },
        { name: 'lastRunReturnCode', required: false, label: 'Last Run Return Code', align: 'left', field: 'lastRunReturnCode', sortable: true, filter: true },
        { name: 'lastRunExecutionGUID', required: false, label: 'Last Execution GUID', align: 'left', field: 'lastRunExecutionGUID', sortable: true, filter: true },
        { name: 'repetitionInterval', required: false, label: 'Repetition', align: 'left', field: 'repetitionInterval', sortable: true, filter: true },
        { name: 'nextScheduledRun', required: false, label: 'Next Run', align: 'left', field: 'nextScheduledRunString', sortable: true, filter: true },
        { name: 'command', required: false, label: 'Command', align: 'left', field: 'command', sortable: true, filter: true },
        { name: 'lastUpdateDate', required: false, label: 'Last Update', align: 'left', field: 'lastUpdateDateString', sortable: true, filter: true },
        { name: '...', required: true, label: '', align: 'left', field: 'guid', sortable: false, filter: false }
      ],
      jobData: [],
      loading: false,
      selectedSecond: []
    }
  },
  methods: {
    request ({ pagination, filter }) {
      var TTT = this
      TTT.loading = true
      var callback = {
        ok: function (response) {
          // console.log(response.data.guid)
          TTT.loading = false

          // updating pagination to reflect in the UI
          TTT.jobsDataTableSettings.serverPagination = pagination
          // we also set (or update) rowsNumber
          TTT.jobsDataTableSettings.serverPagination.rowsNumber = response.data.pagination.total
          TTT.jobsDataTableSettings.serverPagination.filter = filter
          TTT.jobsDataTableSettings.serverPagination.rowsPerPage = response.data.pagination.pagesize

          dataTableSettings.commit('JOBS', TTT.jobsDataTableSettings)

          // then we update the rows with the fetched ones
          TTT.jobData = response.data.result
          TTT.jobData.map(function (obj) {
            obj.creationDateString = userSettings.getters.userTimeStringFN(obj.creationDate)
            obj.nextScheduledRunString = userSettings.getters.userTimeStringFN(obj.nextScheduledRun)
            obj.lastUpdateDateString = userSettings.getters.userTimeStringFN(obj.lastUpdateDate)
            obj.lastRunDateString = userSettings.getters.userTimeStringFN(obj.lastRunDate)
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

      var queryParams = []

      if (filter !== '') {
        queryParams['query'] = filter
      }
      if (pagination.rowsPerPage !== 0) {
        queryParams['pagesize'] = pagination.rowsPerPage.toString()
        queryParams['offset'] = (pagination.rowsPerPage * (pagination.page - 1)).toString()
      }
      if (pagination.sortBy !== null) {
        var postfix = ''
        if (pagination.descending) {
          postfix = ':desc'
        }
        queryParams['sort'] = pagination.sortBy + postfix
      }

      var queryString = restcallutils.buildQueryString('jobs/', queryParams)
      // console.log(queryString)
      globalStore.getters.apiFN('GET', queryString, undefined, callback)
    },
    openCreateJobModalDialog () {
      var child = this.$refs.createJobModalDialog
      var TTTT = this
      child.openCreateJobDialog(function (newJob) {
        var newJobName = newJob.name
        TTTT.jobsDataTableSettings.filter = newJobName
        dataTableSettings.commit('JOBS', TTTT.jobsDataTableSettings)
        TTTT.request({
          pagination: TTTT.jobsDataTableSettings.serverPagination, // Rows number will be overwritten when query returns
          filter: TTTT.jobsDataTableSettings.filter
        })
      })
    },
    deleteJob () {
      var TTT = this
      Dialog.create({
        title: 'Confirm',
        message: 'Delete ' + this.selectedSecond[0].name,
        ok: 'Confirm',
        cancel: 'Cancel'
      }).then(() => {
        var callback = {
          ok: function (response) {
            // console.log(response.data.name)
            TTT.selectedSecond = []
            TTT.request({
              pagination: TTT.jobsDataTableSettings.serverPagination,
              filter: TTT.jobsDataTableSettings.filter
            })
            Notify.create('Job "' + response.data.name + '" Deleted')
          },
          error: function (error) {
            TTT.loading = false
            Notify.create('Job delete failed - ' + callbackHelper.getErrorFromResponse(error))
          }
        }
        globalStore.getters.apiFN('DELETE', 'jobs/' + this.selectedSecond[0].guid, undefined, callback)
      })
    }
  },
  computed: {
    datastoreState () {
      return globalStore.getters.datastoreState
    },
    jobsDataTableSettings () {
      return dataTableSettings.getters.Jobs
    }
  },
  mounted () {
    // once mounted, we need to trigger the initial server data fetch
    this.request({
      pagination: this.jobsDataTableSettings.serverPagination,
      filter: this.jobsDataTableSettings.filter
    })
  }
}
</script>

<style>
</style>
