<template>
  <q-page padding>
    <div>
      <ExecutionTable
        ref="ExecutionTable"
        title="Executions Table"
        DataTableSettingsPrefix='Executions'
        :apiPath="'/executions/'"
      >
      </ExecutionTable>
      <q-btn
        color="primary"
        push
        @click="refreshExecutionData"
      >Refresh</q-btn>
    </div>
  </q-page>
</template>

<script>
import ExecutionTable from '../components/ExecutionTable.vue'

export default {
  name: 'App-Executions',
  components: {
    ExecutionTable
  },
  methods: {
    refreshExecutionData () {
      this.$refs.ExecutionTable.refreshData()
    }
  }
}
</script>
