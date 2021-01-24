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
      selection="multiple"
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
      <selectColumns
        v-model="jobsDataTableSettings.visibleColumns"
        :columns="jobTableColumns"
      />
      <q-input
        v-model="jobsDataTableSettings.filter"
        debounce="500"
        placeholder="Search" outlined
        clearable
      >
        <template v-slot:append>
          <q-icon name="search" />
        </template>
      </q-input>
      </template>

      <q-td  slot="body-cell-name" slot-scope="props" :props="props">
        <q-btn v-if="props.row.mostRecentCompletionStatus === 'Success'" flat color="positive" :label="props.value" @click="$router.push('/jobs/' + props.row.guid)" width="100%"/>
        <q-btn v-if="props.row.mostRecentCompletionStatus === 'Fail'" flat color="negative" :label="props.value" @click="$router.push('/jobs/' + props.row.guid)" width="100%"/>
        <q-btn v-if="props.row.mostRecentCompletionStatus === 'Unknown'" flat color="primary" :label="props.value" @click="$router.push('/jobs/' + props.row.guid)" width="100%"/>
      </q-td>
      <q-td slot="body-cell-..." slot-scope="props" :props="props">
        <q-btn flat color="primary" icon="keyboard_arrow_right" label="" @click="$router.push('/jobs/' + props.row.guid)" />
      </q-td>
      <q-td slot="body-cell-command" slot-scope="props" :props="props">
        <div v-for="curVal in getLineArray(props.value)" :key=curVal.p>{{ curVal.v }}</div>
      </q-td>
      <q-td slot="body-cell-lastRunExecutionGUID" slot-scope="props" :props="props">
        <router-link :to="'/executions/' + props.value" tag="a" class="text-grey-8">
          {{ props.value }}
        </router-link>
      </q-td>
      <q-td slot="body-cell-StateChangeSuccessJobGUID" slot-scope="props" :props="props">
        <router-link :to="'/jobs/' + props.value" tag="a" class="text-grey-8">
          {{ props.row.StateChangeSuccessJobNAME }}
        </router-link>
      </q-td>
      <q-td slot="body-cell-StateChangeFailJobGUID" slot-scope="props" :props="props">
        <router-link :to="'/jobs/' + props.value" tag="a" class="text-grey-8">
          {{ props.row.StateChangeFailJobNAME }}
        </router-link>
      </q-td>
      <q-td slot="body-cell-StateChangeUnknownJobGUID" slot-scope="props" :props="props">
        <router-link :to="'/jobs/' + props.value" tag="a" class="text-grey-8">
          {{ props.row.StateChangeUnknownJobNAME }}
        </router-link>
      </q-td>

    </q-table>
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
import CreateJobModal from '../components/CreateJobModal'
import callbackHelper from '../callbackHelper'
import userSettings from '../store/userSettings'
import restcallutils from '../restcallutils'
import selectColumns from '../components/selectColumns'

export default {
  components: {
    CreateJobModal,
    selectColumns
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
        { name: 'StateChangeSuccessJobGUID', required: false, label: 'State Change Success Job', align: 'left', field: 'StateChangeSuccessJobGUID', sortable: true, filter: true },
        { name: 'StateChangeFailJobGUID', required: false, label: 'State Change Fail Job', align: 'left', field: 'StateChangeFailJobGUID', sortable: true, filter: true },
        { name: 'StateChangeUnknownJobGUID', required: false, label: 'State Change Unknown Job', align: 'left', field: 'StateChangeUnknownJobGUID', sortable: true, filter: true },
        { name: '...', required: true, label: '...', align: 'left', field: 'guid', sortable: false, filter: false }
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
        globalStore.getters.apiFN('DELETE', 'jobs/' + jobItem.guid, undefined, callback)
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
