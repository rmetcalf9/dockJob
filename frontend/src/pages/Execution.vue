<template>
  <div>
    <q-list v-if="loaded">
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
            <router-link :to="'/jobs/' + executionData.jobGUID" class="text-grey-8">
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
import { useServerStaticStateStore } from 'stores/serverStaticState'
import { useLoginStateStore } from 'stores/loginState'

import { Notify } from 'quasar'
import callbackHelper from '../callbackHelper'
import miscFns from '../miscFns'
import STDOutput from '../components/STDOutput.vue'
import callDockjobBackendApi from '../callDockjobBackendApi'

function addDateStringsToExecutionData (obj) {
  obj.dateCreatedString = miscFns.timeString(obj.dateCreated)
  obj.dateStartedString = miscFns.timeString(obj.dateStarted)
  obj.dateCompletedString = miscFns.timeString(obj.dateCompleted)
  return obj
}

export default {
  name: 'App-Execution',
  components: {
    STDOutput
  },
  setup () {
    const serverStaticState = useServerStaticStateStore()
    const loginStateStore = useLoginStateStore()
    return { serverStaticState, loginStateStore }
  },
  data () {
    return {
      loaded: false,
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

      const wrappedCallApiFn = callDockjobBackendApi.getWrappedCallApi({
        loginStateStore: TTT.loginStateStore,
        apiurl: this.serverStaticState.staticServerInfo.data.apiurl
      })

      var executionLoaderCallback = {
        ok: function (response) {
          TTT.executionData = addDateStringsToExecutionData(response.data)
          var jobLoaderCallback = {
            ok: function (response) {
              TTT.loaded = true
              TTT.jobData = response.data
            },
            error: function (error) {
              Notify.create('Loading job data for this exectuion failed - ' + callbackHelper.getErrorFromResponse(error))
              this.jobData = {}
            }
          }
          wrappedCallApiFn({
            method: 'GET',
            path:  '/jobs/' + TTT.executionData.jobGUID,
            postdata: undefined,
            callback: jobLoaderCallback
          })
        },
        error: function (error) {
          Notify.create('Execution query failed - ' + callbackHelper.getErrorFromResponse(error))
          this.jobData = {}
        }
      }
      wrappedCallApiFn({
        method: 'GET',
        path:  '/executions/' + this.$route.params.executionGUID,
        postdata: undefined,
        callback: executionLoaderCallback
      })
    }
  },
  computed: {
  },
  mounted () {
    // once mounted, we need to trigger the initial server data fetch
    this.refreshData()
  }
}
</script>

<style>
</style>
