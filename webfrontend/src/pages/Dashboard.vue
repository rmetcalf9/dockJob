<template>
  <q-page padding class="card-examples row items-start" v-if="datastoreState === 'LOGGED_IN_SERVERDATA_LOADED'">
    <q-card inline class="q-ma-sm">
      <q-card-title>
        Server Info
        <span slot="subtitle">Basic Server Information</span>
      </q-card-title>
      <q-card-main>
        <table>
          <tr><td align="right">Server Startup Time:</td><td>{{ serverInfo.Server.ServerStartupTimeString }}</td></tr>
          <tr><td align="right">Current Time on Server:</td><td>{{ serverInfo.Server.ServerDatetimeString }}</td></tr>
          <tr><td align="right">Total jobs setup:</td><td>{{ serverInfo.Jobs.TotalJobs }}</td></tr>
          <tr><td align="right">Total job executions:</td><td>{{ serverInfo.Server.TotalJobExecutions }}</td></tr>
        </table>
      </q-card-main>
    </q-card>

    <q-card inline class="q-ma-sm">
      <q-card-title>
        Next Run
        <span slot="subtitle">Next Job due to run</span>
      </q-card-title>
      <q-card-main>
        <div v-if='serverInfo.Jobs.NextJobsToExecute.length === 0'>No runs scheduled</div>
        <table v-if='serverInfo.Jobs.NextJobsToExecute.length !== 0'>
          <tr><td align="right">Name:</td><td>
            <router-link :to="'/jobs/' + serverInfo.Jobs.NextJobsToExecute[0].guid" tag="a" class="text-grey-8">
              {{ serverInfo.Jobs.NextJobsToExecute[0].name }}
            </router-link>
          </td></tr>
          <tr><td align="right">When:</td><td>{{ serverInfo.Jobs.NextJobsToExecute[0].nextScheduledRunString }}</td></tr>
        </table>
      </q-card-main>
    </q-card>

    <q-card inline class="q-ma-sm">
      <q-card-title>
        Jobs
        <span slot="subtitle">Job Information</span>
      </q-card-title>
      <q-card-main>
        <table>
          <tr v-for="curVal in jobs" :key=curVal.k>
            <td align="right">{{ curVal.text }}</td><td>{{ curVal.val }}</td>
          </tr>
        </table>
      </q-card-main>
    </q-card>

  </q-page>
</template>

<script>
import globalStore from '../store/globalStore'
import userSettings from '../store/userSettings'

export default {
  data () {
    return {
    }
  },
  methods: {
  },
  computed: {
    jobs () {
      return [
        { k: 1, text: 'Jobs Never Run:', val: globalStore.getters.serverInfo.Jobs.JobsNeverRun },
        { k: 2, text: 'Jobs Completing Sucessfully:', val: globalStore.getters.serverInfo.Jobs.JobsCompletingSucessfully },
        { k: 3, text: 'Jobs where last execution failed:', val: globalStore.getters.serverInfo.Jobs.JobsLastExecutionFailed }
      ]
    },
    serverInfo () {
      var ret = globalStore.getters.serverInfo
      ret.Server.ServerStartupTimeString = userSettings.getters.userTimeStringFN(ret.Server.ServerStartupTime)
      ret.Server.ServerDatetimeString = userSettings.getters.userTimeStringFN(ret.Server.ServerDatetime)
      ret.Jobs.NextJobsToExecute.map(function (obj) {
        obj.nextScheduledRunString = userSettings.getters.userTimeStringFN(obj.nextScheduledRun)
        return obj
      })
      return ret
    },
    datastoreState () {
      return globalStore.getters.datastoreState
    }
  }
}
</script>

<style>
</style>
