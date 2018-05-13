<template>
  <div>
    <q-list >
      <q-item>
        <q-item-main >
          <q-item-tile label>Execution Name:
            {{ executionData.executionName }}
            <span v-if='executionData.manual'>(Manual Run - {{ executionData.stage }})</span>
            <span v-if='!executionData.manual'>(Scheduled Run - {{ executionData.stage }})</span>
          </q-item-tile>
          <q-item-tile sublabel>{{ executionData.guid }}</q-item-tile>
        </q-item-main>
      </q-item>
      <q-item>
        <q-item-main >
          <q-item-tile label>Job: {{ jobData.name }}</q-item-tile>
          <q-item-tile sublabel>
            <router-link :to="'/jobs/' + executionData.jobGUID" tag="a" class="text-grey-8">
              {{ executionData.jobGUID }}
            </router-link>
          </q-item-tile>
        </q-item-main>
      </q-item>
      <q-item>
        <q-item-main >
          <q-item-tile label>Command</q-item-tile>
          <q-item-tile sublabel><div v-for="curVal in getLineArray(executionData.jobCommand)" :key=curVal.p>{{ curVal.v }}</div></q-item-tile>
        </q-item-main>
      </q-item>
      <q-item>
        <q-item-main >
          <q-item-tile label>Stage</q-item-tile>
          <q-item-tile sublabel>{{ executionData.stage }}</q-item-tile>
        </q-item-main>
      </q-item>
      <q-item><q-item-main >
          <q-item-tile label>Creation Date</q-item-tile>
          <q-item-tile sublabel>{{ executionData.dateCreatedString }}</q-item-tile>
      </q-item-main></q-item>
      <q-item><q-item-main >
          <q-item-tile label>Start Date</q-item-tile>
          <q-item-tile sublabel>{{ executionData.dateStartedString }}</q-item-tile>
      </q-item-main></q-item>
      <q-item><q-item-main >
          <q-item-tile label>Completed Date</q-item-tile>
          <q-item-tile sublabel>{{ executionData.dateCompletedString }}</q-item-tile>
      </q-item-main></q-item>
      <q-item><q-item-main >
          <q-item-tile label>Return Code</q-item-tile>
          <q-item-tile sublabel>{{ executionData.resultReturnCode }}</q-item-tile>
      </q-item-main></q-item>
      <q-item><q-item-main >
          <q-item-tile label>Output</q-item-tile>
          <q-item-tile sublabel><STDOutput :val="executionData.resultSTDOUT" /></q-item-tile>
      </q-item-main></q-item>
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
