<template>
<div>
  <q-table
    :title='title'
    :rows="jobExecutionData"
    :columns="jobTableColumns"
    row-key="name"
    :loading="loading"
    @request="requestExecutionData"
    :visible-columns="DataTableSettingsComputed.visibleColumns"
    :filter="DataTableSettingsComputed.filter"
    :pagination="DataTableSettingsComputed.serverPagination"
    @update:pagination="DataTableSettingsComputed.serverPagination = $event"
    :rows-per-page-options="rowsPerPageOptions"
  >
    <template v-slot:top>
      <div class="row col-grow">
         <div class='q-table__title col'>{{ title }}</div>

         <selectColumns
           :valuex="DataTableSettingsComputed.visibleColumns"
           @update:valuex="newValue => DataTableSettingsComputed.visibleColumns = newValue"
           :columns="jobTableColumns"
         />

         <q-input
           v-model="DataTableSettingsComputed.filter"
           debounce="500"
           placeholder="Search" outlined
           clearable
         >
           <template v-slot:append>
             <q-icon name="search" />
           </template>
         </q-input>
      </div>
    </template>

    <template v-slot:body="props">
      <q-tr>
        <q-td v-for="colName in currentlyVisibleColumnNames" v-bind:key="colName">
          <div v-if="colName === 'actions'">
            <q-btn flat color="primary" icon="keyboard_arrow_right" label="" @click="$router.push('/executions/' + props.row.guid)" />
          </div>
          <div v-if="colName === 'jobCommand'">
            <div v-for="curVal in getLineArray(props.row[colName])" :key=curVal.p>{{ curVal.v }}</div>
          </div>
          <div v-if="colName === 'resultSTDOUT'">
            <STDOutput :val="props.row[colName]" maxLinesToShow=3 />
          </div>
          <div v-if="!['resultSTDOUT', 'actions', 'jobCommand'].includes(colName)">{{ props.row[colName] }}</div>
        </q-td>
      </q-tr>
    </template>
  </q-table>
</div>
</template>

<script>
import { useDataTableSettingsStore } from 'stores/dataTableSettings'
import { useLoginStateStore } from 'stores/loginState'
import { useServerStaticStateStore } from 'stores/serverStaticState'
import restcallutils from '../restcallutils'
import callDockjobBackendApi from '../callDockjobBackendApi'
import callbackHelper from '../callbackHelper'
import miscFns from '../miscFns'

import { Loading } from 'quasar'
import { Notify } from 'quasar'

import STDOutput from '../components/STDOutput.vue'
import selectColumns from '../components/selectColumns.vue'

export default {
  name: 'Component-ExecutionTable',
  setup () {
    const dataTableSettings = useDataTableSettingsStore()
    const loginStateStore = useLoginStateStore()
    const serverStaticStateStore = useServerStaticStateStore()
    return { dataTableSettings, loginStateStore, serverStaticStateStore }
  },
  components: {
    STDOutput,
    selectColumns
  },
  props: [
    'title',
    'DataTableSettingsPrefix',
    'apiPath'
  ],
  data () {
    return {
      test: [],
      rowsPerPageOptions: [5, 10, 25, 50, 100, 200],
      jobTableColumns: [
        { name: 'dateStarted', required: false, label: 'Start Date', align: 'left', field: 'dateStartedString', sortable: true, filter: true },
        { name: 'guid', required: false, label: 'Execution GUID', align: 'left', field: 'guid', sortable: true, filter: true },
        { name: 'jobGUID', required: false, label: 'Job GUID', align: 'left', field: 'jobGUID', sortable: true, filter: true },
        { name: 'jobName', required: false, label: 'Job Name', align: 'left', field: 'jobName', sortable: true, filter: true },
        { name: 'executionName', required: false, label: 'Execution Name', align: 'left', field: 'executionName', sortable: true, filter: true },
        { name: 'stage', required: false, label: 'Stage', align: 'left', field: 'stage', sortable: true, filter: true },
        { name: 'resultReturnCode', required: false, label: 'Return Code', align: 'left', field: 'resultReturnCode', sortable: true, filter: true },
        { name: 'manual', required: false, label: 'Manual Run', align: 'left', field: 'manual', sortable: true, filter: true },
        { name: 'dateCreated', required: false, label: 'Creation Date', align: 'left', field: 'dateCreatedString', sortable: true, filter: true },
        { name: 'dateCompleted', required: false, label: 'Completion Date', align: 'left', field: 'dateCompletedString', sortable: true, filter: true },
        { name: 'resultSTDOUT', required: false, label: 'Output', align: 'left', field: 'resultSTDOUT', sortable: true, filter: true },
        { name: 'jobCommand', required: false, label: 'Job Command', align: 'left', field: 'jobCommand', sortable: true, filter: true },
        { name: 'actions', required: true, label: 'Actions', align: 'left', field: 'guid', sortable: false, filter: false }
      ],
      jobExecutionData: [],
      loading: false,
      getLineArray: function (str) {
        if (typeof (str) === 'undefined') return undefined
        var c = 0
        return str.split('\n').map(function (v) { return { p: ++c, v: v } })
      },

    }
  },
  methods: {
    refreshData () {
      this.requestExecutionData({
        pagination: this.DataTableSettingsComputed.serverPagination,
        filter: this.DataTableSettingsComputed.filter
      })
    },
    requestExecutionData ({ pagination, filter }) {
      var TTT = this
      TTT.loading = true
      var callback = {
        ok: function (response) {
          TTT.loading = false

          // updating pagination to reflect in the UI
          TTT.DataTableSettingsComputed.serverPagination = pagination

          // we also set (or update) rowsNumber
          TTT.DataTableSettingsComputed.serverPagination.rowsNumber = response.data.pagination.total
          TTT.DataTableSettingsComputed.serverPagination.filter = filter
          TTT.DataTableSettingsComputed.serverPagination.rowsPerPage = response.data.pagination.pagesize

          // then we update the rows with the fetched ones
          TTT.jobExecutionData = response.data.result
          TTT.jobExecutionData.map(function (obj) {
            obj.dateCreatedString = miscFns.timeString(obj.dateCreated)
            obj.dateStartedString = miscFns.timeString(obj.dateStarted)
            obj.dateCompletedString = miscFns.timeString(obj.dateCompleted)
            return obj
          })

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
      // Filter is not currently working
      //  but this is a BACKEND bug
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
      // Paramaterise this URL
      var queryString = restcallutils.buildQueryString(this.apiPath + '/', queryParams)
      console.log('About to get execution date', queryString)

      const wrappedCallApiFn = callDockjobBackendApi.getWrappedCallApi({
        loginStateStore: TTT.loginStateStore,
        apiurl: TTT.serverStaticStateStore.staticServerInfo.data.apiurl
      })
      wrappedCallApiFn({
        method: 'GET',
        path:  queryString,
        postdata: undefined,
        callback
      })
    }
  },
  computed: {
    DataTableSettingsComputed () {
      return this.dataTableSettings.getSettings({
        name: this.DataTableSettingsPrefix,
        defaultVisibleColumns: ['dateStarted', 'jobName', 'executionName', 'stage', 'resultReturnCode'],
        defaultSortBy: 'dateStarted'
      })
    },
    currentlyVisibleColumnNames () {
      const TTT = this
      return this.jobTableColumns
        .filter(function(x) {
          if (x.required) {
            return true
          }
          return TTT.DataTableSettingsComputed.visibleColumns.includes(x.name)
        })
        .map(function(x) {
          return x.name
        })
    }
  },
  mounted () {
    this.refreshData()
  }
}
</script>
