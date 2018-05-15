<template>
  <div>
    <ExecutionTable
      ref="ExecutionTable"
      title="Executions Table"
      DataTableSettingsPrefix='Executions'
      :apiPath="'executions/'"
    >
    </ExecutionTable>
    <q-btn
      color="primary"
      push
      @click="refreshExecutionData"
    >Refresh</q-btn>
  </div>
  </template>

<script>
// import { Notify, Dialog } from 'quasar'
// import globalStore from '../store/globalStore'
import ExecutionTable from '../components/ExecutionTable'
// import callbackHelper from '../callbackHelper'
// import userSettings from '../store/userSettings'
// import restcallutils from '../restcallutils'

export default {
  components: {
    ExecutionTable
  },
  data () {
    return {
    }
  },
  methods: {
    refreshExecutionData () {
      this.$refs.ExecutionTable.refreshData()
    }
  },
  computed: {
  },
  mounted () {
  }
}
</script>

<style>
</style>
