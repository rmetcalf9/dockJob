<template>
  <div>
    <q-table
      :title='title'
      :data="jobExecutionData"
      :columns="jobTableColumns"
      row-key="name"
      :loading="loading"
      @request="requestExecutionData"
      :visible-columns="DataTableSettings.visibleColumns"
      :filter="DataTableSettings.filter"
      :pagination.sync="DataTableSettings.serverPagination"
      :rows-per-page-options="rowsPerPageOptions"
    >
      <template slot="top-right" slot-scope="props">
        <q-table-columns
          color="secondary"
          class="q-mr-sm"
          v-model="DataTableSettings.visibleColumns"
          :columns="jobTableColumns"
        />
        <q-search clearable hide-underline v-model="DataTableSettings.filter" />
      </template>
      <q-td slot="body-cell-resultSTDOUT" slot-scope="props" :props="props">
        <STDOutput :val="props.value" />
      </q-td>
      <q-td slot="body-cell-jobCommand" slot-scope="props" :props="props">
        <div v-for="curVal in getLineArray(props.value)" :key=curVal.p>{{ curVal.v }}</div>
      </q-td>
    </q-table>
  </div>
</template>

<script>
import { Notify } from 'quasar'
import userSettings from '../store/userSettings'
import callbackHelper from '../callbackHelper'
import restcallutils from '../restcallutils'
import globalStore from '../store/globalStore'
import STDOutput from '../components/STDOutput'
import dataTableSettings from '../store/dataTableSettings'

function addDateStringsToJobData (obj) {
  obj.creationDateString = userSettings.getters.userTimeStringFN(obj.creationDate)
  obj.nextScheduledRunString = userSettings.getters.userTimeStringFN(obj.nextScheduledRun)
  obj.lastUpdateDateString = userSettings.getters.userTimeStringFN(obj.lastUpdateDate)
  obj.lastRunDateString = userSettings.getters.userTimeStringFN(obj.lastRunDate)
  return obj
}

export default {
  components: {
    STDOutput
  },
  props: [
    'title',
    'DataTableSettingsPrefix'
  ],
  data () {
    return {
      rowsPerPageOptions: [5, 10, 25, 50, 100, 200],
      jobTableColumns: [
        { name: 'guid', required: false, label: 'Execution GUID', align: 'left', field: 'guid', sortable: true, filter: true },
        { name: 'executionName', required: false, label: 'Name', align: 'left', field: 'executionName', sortable: true, filter: true },
        { name: 'stage', required: false, label: 'Stage', align: 'left', field: 'stage', sortable: true, filter: true },
        { name: 'resultReturnCode', required: false, label: 'Return Code', align: 'left', field: 'resultReturnCode', sortable: true, filter: true },
        { name: 'manual', required: false, label: 'Manual Run', align: 'left', field: 'manual', sortable: true, filter: true },
        { name: 'dateCreated', required: false, label: 'Creation Date', align: 'left', field: 'dateCreatedString', sortable: true, filter: true },
        { name: 'dateStarted', required: false, label: 'Start Date', align: 'left', field: 'dateStartedString', sortable: true, filter: true },
        { name: 'dateCompleted', required: false, label: 'Completion Date', align: 'left', field: 'dateCompletedString', sortable: true, filter: true },
        { name: 'resultSTDOUT', required: false, label: 'Output', align: 'left', field: 'resultSTDOUT', sortable: true, filter: true },
        { name: 'jobGUID', required: false, label: 'Job GUID', align: 'left', field: 'jobGUID', sortable: true, filter: true },
        { name: 'jobCommand', required: false, label: 'Job Command', align: 'left', field: 'jobCommand', sortable: true, filter: true }
      ],
      jobExecutionData: [],
      loading: false
    }
  },
  methods: {
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
        pagination: this.DataTableSettings.serverPagination,
        filter: this.DataTableSettings.filter
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
          TTT.DataTableSettings.serverPagination = pagination
          // we also set (or update) rowsNumber
          TTT.DataTableSettings.serverPagination.rowsNumber = response.data.pagination.total
          TTT.DataTableSettings.serverPagination.filter = filter
          TTT.DataTableSettings.serverPagination.rowsPerPage = response.data.pagination.pagesize

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

      // TODO Paramaterise this URL
      var queryString = restcallutils.buildQueryString('jobs/' + this.$route.params.jobGUID + '/execution', queryParams)
      // console.log(queryString)
      globalStore.getters.apiFN('GET', queryString, undefined, callback)
    }
  },
  computed: {
    DataTableSettings () {
      return dataTableSettings.getters.prefixedDataTableSetting(this.DataTableSettingsPrefix)
    }

  },
  mounted () {
    // once mounted, we need to trigger the initial server data fetch
    this.refreshJobData()
  }
}
</script>

<style>
</style>
