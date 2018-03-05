<template>
  <div>
    <q-btn
      color="primary"
      push
      @click="openCreateJobModalDialog"
    >Create Job</q-btn>
    <q-table
      title='Jobs'
      :data="jobData"
      :columns="jobTableColumns"
      :filter="filter"
    >
      <template slot="top-left" slot-scope="props">
      </template>
    </q-table>
    <CreateJobModal
      ref="createJobModalDialog"
      v-model="createJobModalDialog"
    />
  </div>

</template>

<script>
// import { Notify } from 'quasar'
import globalStore from '../store/globalStore'
import CreateJobModal from '../components/CreateJobModal'

export default {
  components: {
    CreateJobModal
  },
  data () {
    return {
      createJobModalDialog: {},
      jobTableColumns: [
        {
          name: 'name',
          required: true,
          label: 'Job Name',
          align: 'left',
          field: 'name',
          sortable: true,
          filter: true
        }
      ],
      jobData: [
        {
          name: 'TODO'
        },
        {
          name: 'ANOther'
        }
      ],
      filter: ''
    }
  },
  methods: {
    openCreateJobModalDialog () {
      var child = this.$refs.createJobModalDialog
      child.openCreateJobDialog()
    }
  },
  computed: {
    datastoreState () {
      return globalStore.getters.datastoreState
    }
  }
}
</script>

<style>
</style>
