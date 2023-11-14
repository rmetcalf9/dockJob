<template>
  <q-page padding class="card-examples row items-start" v-if="serverStateLoaded">
    <q-card inline class="q-ma-sm">
      <q-card-section>
        <div class="text-h6">Server Info</div>
        <div class="text-subtitle2">Basic Server Information</div>
      </q-card-section>
      <q-card-section>
        <table>
          <tr><td align="right">Server Startup Time:</td><td>{{ serverInfo.Server.ServerStartupTimeString }}</td></tr>
          <tr><td align="right">Current Time on Server:</td><td>{{ serverInfo.Server.ServerDatetimeString }}</td></tr>
          <tr><td align="right">Total jobs setup:</td><td>{{ serverInfo.Jobs.TotalJobs }}</td></tr>
          <tr><td align="right">Total job executions:</td><td>{{ serverInfo.Server.TotalJobExecutions }}</td></tr>
        </table>
      </q-card-section>
    </q-card>

    <q-card inline class="q-ma-sm">
      <q-card-section>
        <div class="text-h6">Next Run</div>
        <div class="text-subtitle2">Next Job due to run</div>
      </q-card-section>
      <q-card-section>
        <div v-if='serverInfo.Jobs.NextJobsToExecute.length === 0'>No runs scheduled</div>
        <table v-if='serverInfo.Jobs.NextJobsToExecute.length !== 0'>
          <tr><td align="right">Name:</td><td>
            <router-link custom :to="'/jobs/' + serverInfo.Jobs.NextJobsToExecute[0].guid" class="text-grey-8">
              {{ serverInfo.Jobs.NextJobsToExecute[0].name }}
            </router-link>

<!--            <router-link :to="'/jobs/' + serverInfo.Jobs.NextJobsToExecute[0].guid" tag="a" class="text-grey-8">
              {{ serverInfo.Jobs.NextJobsToExecute[0].name }}
            </router-link>-->
          </td></tr>
          <tr><td align="right">When:</td><td>{{ serverInfo.Jobs.NextJobsToExecute[0].nextScheduledRunString }}</td></tr>
        </table>
      </q-card-section>
    </q-card>

    <q-card inline class="q-ma-sm">
      <q-card-section>
        <div class="text-h6">Jobs</div>
        <div class="text-subtitle2">Job Information</div>
      </q-card-section>
      <q-card-section>
        <table>
          <tr v-for="curVal in jobs" :key=curVal.k>
            <td align="right">{{ curVal.text }}</td><td>{{ curVal.val }}</td>
          </tr>
        </table>
      </q-card-section>
    </q-card>
    <div v-for="curJob in pinnedJobs" :key=curJob.guid>
      <q-card inline :class="'q-ma-sm ' + getCardClass(curJob)">
        <q-card-section>
          <div class="text-h6">{{ curJob.name }}</div>
          <div class="text-subtitle2">{{ curJob.mostRecentCompletionStatus }}</div>
        </q-card-section>
        <q-card-section>
          <table>
            <tr><td align="right">Manual:</td><td>{{ !curJob.enabled }}</td></tr>
            <tr><td align="right">Last Run:</td><td>{{ curJob.lastRunDate }}</td></tr>
            <tr><td align="right">Return Code:</td><td>{{ curJob.lastRunReturnCode }}</td></tr>
          </table>
        </q-card-section>
        <q-card-actions>
          <q-btn flat round dense icon="rowing" @click="$router.push('/jobs/' + curJob.guid)" />
          <q-btn flat round dense icon="play_arrow" @click="runnow(curJob.guid, curJob.name)" />
        </q-card-actions>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { useServerStaticStateStore } from 'stores/serverStaticState'
import { useServerInfoStore } from 'stores/serverInfo'
import { useLoginStateStore } from 'stores/loginState'
import callDockjobBackendApi from '../callDockjobBackendApi'

import { Notify } from 'quasar'

export default {
  name: 'App-Dashboard',
  data () {
    return {
      pinnedJobs: [{guid: 'a'}, {guid: 'b'}, {guid: 'c'}]
    }
  },
  setup () {
    const serverStaticState = useServerStaticStateStore()
    const serverInfoStore = useServerInfoStore()
    const loginStateStore = useLoginStateStore()
    return { serverStaticState, serverInfoStore, loginStateStore }
  },
  computed: {
    serverStateLoaded () {
      if (!this.serverStaticState.isLoaded) {
        return false
      }
      return this.serverInfoStore.isLoaded
    },
    serverInfo () {
      var ret = this.serverInfoStore.serverInfo
      // ret.Server.ServerStartupTimeString = userSettings.getters.userTimeStringFN(ret.Server.ServerStartupTime)
      // ret.Server.ServerDatetimeString = userSettings.getters.userTimeStringFN(ret.Server.ServerDatetime)
      // ret.Jobs.NextJobsToExecute.map(function (obj) {
      //  obj.nextScheduledRunString = userSettings.getters.userTimeStringFN(obj.nextScheduledRun)
      //  return obj
      // })
      return ret
    },
  },
  methods: {
    getCardClass (jobObj) {
      // TODO put back
      // if (jobObj.mostRecentCompletionStatus === 'Success') {
      //  return 'bg-positive'
      // }
      // if (jobObj.mostRecentCompletionStatus === 'Fail') {
      //  return 'bg-negative'
      // }
      return 'bg-primary'
    },
    refreshPage ({wait}) {
      const TTT=this
      if (!this.serverStaticState.isLoaded) {
        if (wait>0) {
          setTimeout(function(){
              TTT.refreshPage({wait: wait - 1})
          }, 100);
        }
        return
      }
      const callback = {
        ok: function (response) {
          TTT.refreshJobs()
        },
        error: function (error) {
          console.log('Refresh server info failed', error)
          Notify.create({
            color: 'negative',
            message: 'Refresh server info failed' + error
          })
        }
      }
      const wrappedCallApiFn = callDockjobBackendApi.getWrappedCallApi({
        loginStateStore: TTT.loginStateStore,
        apiurl: this.serverStaticState.staticServerInfo.data.apiurl
      })
      this.serverInfoStore.refresh({force: true, callback, wrappedCallApiFn})
    },
    refreshJobs () {
      console.log('TODO REFRESH JOBS')
    }
  },
  mounted () {
    this.refreshPage({wait: 5})
  }
}
</script>
