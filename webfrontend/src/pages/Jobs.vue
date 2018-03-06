<template>
  <div>
    <q-table
      title='Jobs'
      :data="jobData"
      :columns="jobTableColumns"
      :visible-columns="visibleColumns"
      :filter="filter"
      row-key="name"
      :pagination.sync="serverPagination"
      :loading="loading"
      @request="request"
    >
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
        v-model="visibleColumns"
        :columns="jobTableColumns"
      />
      <q-search hide-underline v-model="filter" />
      </template>
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
import CreateJobModal from '../components/CreateJobModal'
import callbackHelper from '../callbackHelper'

export default {
  components: {
    CreateJobModal
  },
  data () {
    return {
      createJobModalDialog: {},
      jobTableColumns: [
        // { name: 'guid', required: false, label: 'GUID', align: 'left', field: 'guid', sortable: false, filter: true },
        { name: 'name', required: true, label: 'Job Name', align: 'left', field: 'name', sortable: false, filter: true },
        { name: 'enabled', required: false, label: 'Enabled', align: 'left', field: 'enabled', sortable: false, filter: true },
        { name: 'creationDate', required: false, label: 'Created', align: 'left', field: 'creationDate', sortable: false, filter: true },
        { name: 'lastRunDate', required: false, label: 'Last Run', align: 'left', field: 'lastRunDate', sortable: false, filter: true },
        { name: 'repetitionInterval', required: false, label: 'Repetition', align: 'left', field: 'repetitionInterval', sortable: false, filter: true },
        { name: 'nextScheduledRun', required: false, label: 'Next Run', align: 'left', field: 'nextScheduledRun', sortable: false, filter: true },
        { name: 'command', required: false, label: 'Command', align: 'left', field: 'command', sortable: false, filter: true },
        { name: 'lastUpdateDate', required: false, label: 'Last Update', align: 'left', field: 'lastUpdateDate', sortable: false, filter: true }
      ],
      jobData: [],
      filter: '',
      loading: false,
      serverPagination: {
        page: 1,
        rowsNumber: 10 // specifying this determines pagination is server-side
      },
      visibleColumns: ['name', 'enabled', 'nextScheduledRun']
    }
  },
  methods: {
    request ({ pagination, filter }) {
      var TTT = this
      TTT.loading = true
      // console.log('request')
      // console.log(pagination)
      // pagination = {
      //   descending:false
      //   page:2
      //   rowsNumber:10
      //   rowsPerPage:5
      //   sortBy:null
      // }
      // console.log(filter) (String)
      var callback = {
        ok: function (response) {
          // console.log(response.data.guid)
          TTT.loading = false
          // updating pagination to reflect in the UI
          TTT.serverPagination = pagination

          // we also set (or update) rowsNumber
          TTT.serverPagination.rowsNumber = response.data.pagination.total

          // then we update the rows with the fetched ones
          TTT.jobData = response.data.result

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
      var queryString = 'jobs/?pagesize=' + pagination.rowsPerPage.toString() + '&offset=' + (pagination.rowsPerPage * (pagination.page - 1)).toString()
      if (filter !== '') {
        queryString = 'jobs/?pagesize=' + pagination.rowsPerPage.toString() + '&query=' + filter + '&offset=' + (pagination.rowsPerPage * (pagination.page - 1)).toString()
      }
      globalStore.getters.apiFN('GET', queryString, undefined, callback)
    },
    openCreateJobModalDialog () {
      var child = this.$refs.createJobModalDialog
      var TTTT = this
      child.openCreateJobDialog(function (newJobName) {
        TTTT.filter = newJobName
        TTTT.request({
          pagination: TTTT.serverPagination, // Rows number will be overwritten when query returns
          filter: TTTT.filter
        })
      })
    }
  },
  computed: {
    datastoreState () {
      return globalStore.getters.datastoreState
    }
  },
  mounted () {
    // once mounted, we need to trigger the initial server data fetch
    this.request({
      pagination: this.serverPagination,
      filter: this.filter
    })
  }
}
</script>

<style>
</style>
