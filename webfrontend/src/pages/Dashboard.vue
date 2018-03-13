<template>
  <div class="layout-padding card-examples row items-start" v-if="datastoreState === 'LOGGED_IN_SERVERDATA_LOADED'">
    <q-card inline>
      <q-card-title>
        Server Info
        <span slot="subtitle">Basic Server Information</span>
      </q-card-title>
      <q-card-main>
        <table>
          <tr><td align="right">Server Startup Time:</td><td>{{ serverInfo.Server.ServerStartupTime }}</td></tr>
          <tr><td align="right">Current Time on Server:</td><td>{{ serverInfo.Server.ServerDatetime }}</td></tr>
          <tr><td align="right">Total jobs setup:</td><td>{{ serverInfo.Jobs.TotalJobs }}</td></tr>
        </table>
      </q-card-main>
    </q-card>

    <q-card inline>
      <q-card-title>
        Next Run
        <span slot="subtitle">Next Job due to run</span>
      </q-card-title>
      <q-card-main>
        Job Name, Date Time, How Long
      </q-card-main>
    </q-card>

    <q-card inline>
      <q-card-title>
        Job Logs
        <span slot="subtitle">Job results</span>
      </q-card-title>
      <q-card-main>
        Successfully completed, Errored
      </q-card-main>
    </q-card>

  </div>
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
