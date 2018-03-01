<template>
  <div>
    <q-btn
      color="primary"
      push
      @click="createJob"
    >Create Job</q-btn>
  <q-data-table
    :data="jobData"
    :columns="jobTableColumns"
    :config="tableConfig"
    :filter="filter"
  >
    <template slot="top-left" slot-scope="props">
      <q-search
        hide-underline
        color="secondary"
        v-model="filter"
        class="col-6"
      />
    </template>
  </q-data-table>

  </div>
</template>

<script>
import {
  QBtn,
  QDataTable,
  QSearch
} from 'quasar'
import globalStore from '../stores/globalStore'

export default {
  components: {
    QBtn,
    QDataTable,
    QSearch
  },
  data () {
    return {
      tableConfig: {
        columnPicker: true,
        pagination: {
          rowsPerPage: 15,
          options: [5, 10, 15, 30, 50, 500]
        }
      },
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
