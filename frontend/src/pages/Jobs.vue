<template>
  <div>
    <q-table
      title='Jobs'
      :rows="jobData"
      :columns="jobTableColumns"
      :visible-columns="DataTableSettingsComputed.visibleColumns"
      :filter="DataTableSettingsComputed.filter"
      row-key="name"
      :pagination="DataTableSettingsComputed.serverPagination"
      @update:pagination="DataTableSettingsComputed.serverPagination = $event"
      :loading="loading"
      @request="request"
      selection="multiple"
      :selected="selectedSecond"
      @update:selected="selectedSecond = $event"
      :rows-per-page-options="rowsPerPageOptions"
    >
    <template v-slot:top>
      <div v-if="selectedSecond.length !== 0">
        <q-btn flat round delete icon="delete" @click="deleteJob" />
      </div>
      <div v-if="selectedSecond.length === 0">
          <q-btn
            color="primary"
            push
            @click="openCreateJobModalDialog"
          >Create Job</q-btn>
      </div>
      <div class="row col-grow">
         <div class='q-table__title col'>Jobs</div>
      </div>
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
    </template>

    <template v-slot:body="props">
      <q-tr>
        <q-td>
          <q-checkbox v-model="props.selected" />
        </q-td>
        <q-td v-for="colName in currentlyVisibleColumnNames" v-bind:key="colName">
          <div v-if="colName === 'actions'">
            <q-btn flat color="primary" icon="keyboard_arrow_right" label="" @click="$router.push('/jobs/' + props.row.guid)" />
          </div>
          <div v-if="colName === 'command'">
            <div v-for="curVal in getLineArray(props.row[colName])" :key=curVal.p>{{ curVal.v }}</div>
          </div>
          <div v-if="colName === 'name'">
            <q-btn v-if="props.row.mostRecentCompletionStatus === 'Success'" flat color="positive" :label="props.row[colName]" @click="$router.push('/jobs/' + props.row.guid)" width="100%"/>
            <q-btn v-if="props.row.mostRecentCompletionStatus === 'Fail'" flat color="negative" :label="props.row[colName]" @click="$router.push('/jobs/' + props.row.guid)" width="100%"/>
            <q-btn v-if="props.row.mostRecentCompletionStatus === 'Unknown'" flat color="primary" :label="props.row[colName]" @click="$router.push('/jobs/' + props.row.guid)" width="100%"/>
          </div>
          <div v-if="colName === 'lastRunExecutionGUID'">
            <router-link :to="'/executions/' + props.row[colName]" class="text-grey-8">
              {{ props.row[colName] }}
            </router-link>
          </div>

          <div v-if="!['lastRunExecutionGUID', 'name', 'actions', 'command'].includes(colName)">
            <div v-if="props.colsMap[colName].linkToOtherJob">
              <div v-if="props.row[colName] && props.row[colName].length > 0">
                <router-link :to="'/jobs/' + props.row[colName]" class="text-grey-8">
                  {{ props.row[colName.substring(0, colName.length-4) + 'NAME'] }}
                </router-link>
              </div>
            </div>
            <div v-if="!props.colsMap[colName].linkToOtherJob">
              {{ props.row[colName] }}
            </div>
          </div>
        </q-td>
      </q-tr>
    </template>
    </q-table>
    <CreateJobModal
      ref="createJobModalDialog"
    />
  </div>

</template>

<script>
import { Notify } from 'quasar'
import { useDataTableSettingsStore } from 'stores/dataTableSettings'
import { useLoginStateStore } from 'stores/loginState'
import { useServerStaticStateStore } from 'stores/serverStaticState'
import callbackHelper from '../callbackHelper'
import miscFns from '../miscFns'
import restcallutils from '../restcallutils'
import callDockjobBackendApi from '../callDockjobBackendApi'

import CreateJobModal from '../components/CreateJobModal.vue'
import selectColumns from '../components/selectColumns.vue'

const dataTableSettingsName='Jobs'

export default {
  name: 'App-Jobs',
  components: {
    CreateJobModal,
    selectColumns
  },
  setup () {
    const dataTableSettings = useDataTableSettingsStore()
    const loginStateStore = useLoginStateStore()
    const serverStaticStateStore = useServerStaticStateStore()
    return { dataTableSettings, loginStateStore, serverStaticStateStore }
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
        { name: 'mostRecentCompletionStatus', required: false, label: 'Completion Status', align: 'left', field: 'mostRecentCompletionStatus', sortable: true, filter: true },
        { name: 'pinned', required: false, label: 'Pinned', align: 'left', field: 'pinned', sortable: true, filter: true },
        { name: 'overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown', required: false, label: 'Unknown Timeout', align: 'left', field: 'overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown', sortable: true, filter: true },
        { name: 'StateChangeSuccessJobGUID', required: false, label: 'State Change Success Job', align: 'left', field: 'StateChangeSuccessJobGUID', sortable: true, filter: true, linkToOtherJob: true },
        { name: 'StateChangeFailJobGUID', required: false, label: 'State Change Fail Job', align: 'left', field: 'StateChangeFailJobGUID', sortable: true, filter: true, linkToOtherJob: true },
        { name: 'StateChangeUnknownJobGUID', required: false, label: 'State Change Unknown Job', align: 'left', field: 'StateChangeUnknownJobGUID', sortable: true, filter: true, linkToOtherJob: true },
        { name: 'AfterSuccessJobGUID', required: false, label: 'After Success Job', align: 'left', field: 'AfterSuccessJobGUID', sortable: true, filter: true, linkToOtherJob: true },
        { name: 'AfterFailJobGUID', required: false, label: 'After Fail Job', align: 'left', field: 'AfterFailJobGUID', sortable: true, filter: true, linkToOtherJob: true },
        { name: 'AfterUnknownJobGUID', required: false, label: 'After Unknown Job', align: 'left', field: 'AfterUnknownJobGUID', sortable: true, filter: true, linkToOtherJob: true },
        { name: 'actions', required: true, label: '...', align: 'left', field: 'guid', sortable: false, filter: false }
      ],
      jobData: [],
      loading: false,
      selectedSecond: [],
      localTableVisibleColumns: []
    }
  },
  methods: {
    request ({ pagination, filter }) {
      var TTT = this
      TTT.loading = true
      var callback = {
        ok: function (response) {
          // console.log(response.data.guid)

          // updating pagination to reflect in the UI
          TTT.DataTableSettingsComputed.serverPagination = pagination
          // we also set (or update) rowsNumber
          TTT.DataTableSettingsComputed.serverPagination.rowsNumber = response.data.pagination.total
          TTT.DataTableSettingsComputed.serverPagination.filter = filter
          TTT.DataTableSettingsComputed.serverPagination.rowsPerPage = response.data.pagination.pagesize

          //dataTableSettingsName
          TTT.dataTableSettings.saveSettings({
            name: dataTableSettingsName,
            newSettings: TTT.DataTableSettingsComputed
          })

          // then we update the rows with the fetched ones
          TTT.jobData = response.data.result
          TTT.jobData.map(function (obj) {
            obj.creationDateString = miscFns.timeString(obj.creationDate)
            obj.nextScheduledRunString = miscFns.timeString(obj.nextScheduledRun)
            obj.lastUpdateDateString = miscFns.timeString(obj.lastUpdateDate)
            obj.lastRunDateString = miscFns.timeString(obj.lastRunDate)
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
        if (filter !== null) {
          queryParams['query'] = filter
        }
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

      var queryString = restcallutils.buildQueryString('/jobs/', queryParams)
      // console.log(queryString)

      const wrappedCallApiFn = callDockjobBackendApi.getWrappedCallApi({
        loginStateStore: TTT.loginStateStore,
        apiurl: TTT.serverStaticStateStore.staticServerInfo.data.apiurl
      })
      wrappedCallApiFn({
        method: 'GET',
        path:  queryString,
        postdata: undefined,
        callback: callback
      })
    },
    openCreateJobModalDialog () {
      var child = this.$refs.createJobModalDialog
      var TTTT = this
      child.openCreateJobDialog(function (newJob) {
        var newJobName = newJob.name
        TTTT.DataTableSettingsComputed.filter = newJobName
        TTTT.dataTableSettings.saveSettings({
          name: dataTableSettingsName,
          newSettings: TTTT.DataTableSettingsComputed
        })
        TTTT.request({
          pagination: TTTT.DataTableSettingsComputed.serverPagination, // Rows number will be overwritten when query returns
          filter: TTTT.DataTableSettingsComputed.filter
        })
      })
    },
    deleteJob () {
      var TTT = this
      if (TTT.selectedSecond.length === 0) {
        return
      }
      var msg = ''
      if (TTT.selectedSecond.length === 1) {
        msg = 'Are you sure you want to delete ' + TTT.selectedSecond[0].name
      } else {
        msg = 'Are you sure you want to delete ' + TTT.selectedSecond.length + ' jobs'
      }
      TTT.getConfirmedActionFn(
        msg,
        undefined,
        TTT.deleteJobConfirmed
      )()
    },
    deleteJobConfirmed () {
      var TTT = this
      TTT.selectedSecond.map(function (jobItem) {
        var callback = {
          ok: function (response) {
            Notify.create({color: 'positive', message: 'Job "' + response.data.name + '" Deleted'})
            TTT.jobData = TTT.jobData.filter(function (jobDataItem) {
              return jobDataItem.guid !== jobItem.guid
            })
          },
          error: function (error) {
            Notify.create({color: 'negetive', message: 'Job delete failed - ' + callbackHelper.getErrorFromResponse(error)})
          }
        }
        const wrappedCallApiFn = callDockjobBackendApi.getWrappedCallApi({
          loginStateStore: TTT.loginStateStore,
          apiurl: TTT.serverStaticStateStore.staticServerInfo.data.apiurl
        })
        wrappedCallApiFn({
          method: 'DELETE',
          path:  '/jobs/' + jobItem.guid,
          postdata: undefined,
          callback: callback
        })
      })
      TTT.selectedSecond = []
    },
    getConfirmedActionFn (text, param, fn) {
      var TTT = this
      return function (event) {
        TTT.$q.dialog({
          title: 'Confirm',
          message: text,
          ok: {
            push: true,
            label: 'Yes'
          },
          cancel: {
            push: true,
            label: 'Cancel'
          }
          // preventClose: false,TTT._GetLinkText(link)
          // noBackdropDismiss: false,
          // noEscDismiss: false
        }).onOk(() => {
          fn(event, param)
        })
      }
    },
    refresh () {
      this.request({
        pagination: this.DataTableSettingsComputed.serverPagination,
        filter: this.DataTableSettingsComputed.filter
      })
    }
  },
  computed: {
    DataTableSettingsComputed () {
      return this.dataTableSettings.getSettings({
        name: dataTableSettingsName,
        defaultVisibleColumns: ['name', 'enabled', 'lastRunReturnCode', 'nextScheduledRun'],
        defaultSortBy: null
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
    // once mounted, we need to trigger the initial server data fetch
    this.refresh()
  }
}
</script>

<style>
</style>
