<template>
  <div>
    <q-list >
      <q-item>
        <q-item-section v-if='executionData.executionName.length > 0'>
          <q-item-label>Execution Name: {{ executionData.executionName }}</q-item-label>
          <q-item-label caption v-if='executionData.manual'>(Manual Run - {{ executionData.stage }})</q-item-label>
          <q-item-label caption v-if='!executionData.manual'>(Scheduled Run - {{ executionData.stage }})</q-item-label>
          <q-item-label>{{ executionData.guid }}</q-item-label>
        </q-item-section>
        <q-item-section v-if='executionData.executionName.length === 0'>
          <q-item-label>Unnamed execution</q-item-label>
          <q-item-label caption v-if='executionData.manual'>(Manual Run - {{ executionData.stage }})</q-item-label>
          <q-item-label caption v-if='!executionData.manual'>(Scheduled Run - {{ executionData.stage }})</q-item-label>
          <q-item-label>{{ executionData.guid }}</q-item-label>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section>
          <q-item-label>Job: {{ jobData.name }}</q-item-label>
          <q-item-label caption>
            <router-link :to="'/jobs/' + executionData.jobGUID" tag="a" class="text-grey-8">
              {{ executionData.jobGUID }}
            </router-link>
          </q-item-label>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section>
          <q-item-label>Command</q-item-label>
          <q-item-label caption>
            <div v-for="curVal in getLineArray(executionData.jobCommand)" :key="curVal.p">{{ curVal.v }}</div>
          </q-item-label>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section >
          <q-item-label>Stage</q-item-label>
          <q-item-label caption>{{ executionData.stage }}</q-item-label>
        </q-item-section>
      </q-item>
      <q-item><q-item-section >
          <q-item-label>Creation Date</q-item-label>
          <q-item-label caption>{{ executionData.dateCreatedString }}</q-item-label>
      </q-item-section></q-item>
      <q-item><q-item-section >
          <q-item-label>Start Date</q-item-label>
          <q-item-label caption>{{ executionData.dateStartedString }}</q-item-label>
      </q-item-section></q-item>
      <q-item><q-item-section >
          <q-item-label>Completed Date</q-item-label>
          <q-item-label caption>{{ executionData.dateCompletedString }}</q-item-label>
      </q-item-section></q-item>
      <q-item><q-item-section >
          <q-item-label>Return Code</q-item-label>
          <q-item-label caption>{{ executionData.resultReturnCode }}</q-item-label>
      </q-item-section></q-item>
      <q-item><q-item-section >
          <q-item-label>Output</q-item-label>
          <q-item-label caption><STDOutput :val="executionData.resultSTDOUT" /></q-item-label>
      </q-item-section></q-item>
    </q-list>
  </div>
</template>

<script>
import { Notify } from 'quasar'
import globalStore from '../store/globalStore'
import callbackHelper from '../callbackHelper'
import userSettings from '../store/userSettings'
import STDOutput from '../components/STDOutput'

function addDateStringsToExecutionData (obj) {
  obj.dateCreatedString = userSettings.getters.userTimeStringFN(obj.dateCreated)
  obj.dateStartedString = userSettings.getters.userTimeStringFN(obj.dateStarted)
  obj.dateCompletedString = userSettings.getters.userTimeStringFN(obj.dateCompleted)
  return obj
}

export default {
  components: {
    STDOutput
  },
  data () {
    return {
      executionData: {},
      jobData: {},
      getLineArray: function (str) {
        if (typeof (str) === 'undefined') return undefined
        var c = 0
        return str.split('\n').map(function (v) { return { p: ++c, v: v } })
      }
    }
  },
  methods: {
    refreshData () {
      // Will load the execution data
      //  then make second call to load the job data
      var TTT = this
      var executionLoaderCallback = {
        ok: function (response) {
          TTT.executionData = addDateStringsToExecutionData(response.data)
          if (typeof (TTT.executionData.executionName.length) !== 'undefined') {
            if (TTT.executionData.executionName.length > 0) {
              globalStore.commit('SET_PAGE_TITLE', 'Execution ' + TTT.executionData.executionName)
            }
          }
          var jobLoaderCallback = {
            ok: function (response) {
              TTT.jobData = response.data
            },
            error: function (error) {
              Notify.create('Loading job data for this exectuion failed - ' + callbackHelper.getErrorFromResponse(error))
              this.jobData = {}
            }
          }
          globalStore.getters.apiFN('GET', 'jobs/' + TTT.executionData.jobGUID, undefined, jobLoaderCallback)
        },
        error: function (error) {
          Notify.create('Execution query failed - ' + callbackHelper.getErrorFromResponse(error))
          this.jobData = {}
        }
      }
      globalStore.getters.apiFN('GET', 'executions/' + this.$route.params.executionGUID, undefined, executionLoaderCallback)
    }
  },
  computed: {
  },
  mounted () {
    // once mounted, we need to trigger the initial server data fetch
    globalStore.commit('SET_PAGE_TITLE', 'Execution ' + this.$route.params.executionGUID)
    this.refreshData()
  }
}
</script>

<style>
</style>
