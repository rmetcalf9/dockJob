<template>
  <div>
    <q-btn
      color="primary"
      push
      @click="createJob"
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

  </div>
</template>

<script>
import globalStore from '../store/globalStore'

export default {
  data () {
    return {
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
    createJob () {
      console.log('TODO')
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
