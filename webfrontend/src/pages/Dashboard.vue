<template>
  <q-page padding class="card-examples row items-start" v-if="datastoreState === 'LOGGED_IN_SERVERDATA_LOADED'">
    <q-card inline class="q-ma-sm">
      <q-card-title>
        Server Info
        <span slot="subtitle">Basic Server Information</span>
      </q-card-title>
      <q-card-main>
        <table>
          <tr><td align="right">Server Startup Time:</td><td>{{ serverInfo.Server.ServerStartupTime }}</td></tr>
          <tr><td align="right">Current Time on Server:</td><td>{{ serverInfo.Server.ServerDatetime }}</td></tr>
          <tr><td align="right">Total jobs setup:</td><td>{{ serverInfo.Jobs.TotalJobs }}</td></tr>
          <tr><td align="right">Total jobs executed:</td><td>{{ serverInfo.Server.TotalJobExecutions }}</td></tr>
        </table>
      </q-card-main>
    </q-card>

    <q-card inline class="q-ma-sm">
      <q-card-title>
        Next Run
        <span slot="subtitle">Next Job due to run</span>
      </q-card-title>
      <q-card-main>
        <table>
          <tr><td align="right">Name:</td><td>
            <router-link :to="'/jobs/' + serverInfo.Jobs.NextJobsToExecute[0].guid" tag="a" class="text-grey-8">
              {{ serverInfo.Jobs.NextJobsToExecute[0].name }}
            </router-link>
          </td></tr>
          <tr><td align="right">When:</td><td>{{ serverInfo.Jobs.NextJobsToExecute[0].nextScheduledRun }}</td></tr>
        </table>
      </q-card-main>
    </q-card>

    <q-card inline class="q-ma-sm">
      <q-card-title>
        Job Logs
        <span slot="subtitle">Job results</span>
      </q-card-title>
      <q-card-main>
        Successfully completed, Errored
      </q-card-main>
    </q-card>

  </q-page>
</template>

<script>
import globalStore from '../store/globalStore'

export default {
  data () {
    return {
    }
  },
  methods: {
  },
  computed: {
    serverInfo () {
      return globalStore.getters.serverInfo
    },
    datastoreState () {
      return globalStore.getters.datastoreState
    }
  }
}
</script>

<style>
</style>
