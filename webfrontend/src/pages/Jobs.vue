<template>
  <div>
    <q-table
      title='Jobs'
      :data="jobData"
      :columns="jobTableColumns"
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
        { name: 'name', required: true, label: 'Job Name', align: 'left', field: 'name', sortable: false, filter: true }
      ],
      jobData: [],
      filter: '',
      loading: false,
      serverPagination: {
        page: 1,
        rowsNumber: 10 // specifying this determines pagination is server-side
      }
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
      var queryString = 'jobs/?pagesize=' + pagination.rowsPerPage.toString() + '&offset=' + (pagination.rowsPerPage * (pagination.page - 1)).toString()
      if (filter !== '') {
        queryString = 'jobs/?pagesize=' + pagination.rowsPerPage.toString() + '&query=' + filter + '&offset=' + (pagination.rowsPerPage * (pagination.page - 1)).toString()
      }
      globalStore.getters.apiFN('GET', queryString, undefined, callback)
    },
    openCreateJobModalDialog () {
      var child = this.$refs.createJobModalDialog
      child.openCreateJobDialog()
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
