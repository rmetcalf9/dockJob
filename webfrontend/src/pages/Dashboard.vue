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
    <div v-for="curJob in pinnedJobs" :key=curJob.guid>
      <q-card inline :class="'q-ma-sm ' + getCardClass(curJob)">
        <q-card-title>
         {{ curJob.name }}
          <span slot="subtitle">{{ curJob.mostRecentCompletionStatus }}</span>
        </q-card-title>
        <q-card-main>
          <table>
            <tr><td align="right">Manual:</td><td>{{ !curJob.enabled }}</td></tr>
            <tr><td align="right">Last Run:</td><td>{{ curJob.lastRunDate }}</td></tr>
            <tr><td align="right">Return Code:</td><td>{{ curJob.lastRunReturnCode }}</td></tr>
          </table>
        </q-card-main>
        <q-card-actions>
          <q-btn flat round dense icon="rowing" @click="$router.push('/jobs/' + curJob.guid)" />
          <q-btn flat round dense icon="play_arrow" @click="runnow(curJob.guid, curJob.name)" />
        </q-card-actions>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import globalStore from '../store/globalStore'
import userSettings from '../store/userSettings'
import { Notify, Loading } from 'quasar'
import callbackHelper from '../callbackHelper'
import getDepaginatedQueryResults from '../depaginatedQuery.js'

export default {
  data () {
    return {
      pinnedJobs: [{guid: 'a'}, {guid: 'b'}, {guid: 'c'}]
    }
  },
  methods: {
    runnow (jobGUID, jobName) {
      var callback = {
        ok: function (response) {
          Notify.create({color: 'positive', detail: 'Job Execution Request Sent'})
          // this.refreshJobData() No point doing this immediately
        },
        error: function (error) {
          Notify.create('Request for execution failed - ' + callbackHelper.getErrorFromResponse(error))
        }
      }
      this.$q.dialog({
        title: 'Submit request to run ' + jobName,
        message: 'Name for execution',
        prompt: {
          model: '',
          type: 'text' // optional
        },
        cancel: true,
        color: 'secondary'
      }).then(data => {
        var params = {name: data}
        globalStore.getters.apiFN('POST', 'jobs/' + jobGUID + '/execution', params, callback)
      })
    },
    getCardClass (jobObj) {
      if (jobObj.mostRecentCompletionStatus === 'Success') {
        return 'bg-positive'
      }
      if (jobObj.mostRecentCompletionStatus === 'Fail') {
        return 'bg-negative'
      }
      return 'bg-primary'
    },
    refreshPage () {
      // refreshes pinned jobs
      var TTT = this
      var callback = {
        ok: function (response) {
          // console.log(response.data.guid)
          Loading.hide()

          TTT.pinnedJobs = response.data.result

          TTT.loading = false

          if (!response.data.dePaginatorResp.complete) {
            Notify.create({color: 'info', detail: 'Not all pinned jobs were queried back'})
          }
        },
        error: function (error) {
          Loading.hide()
          Notify.create('Failed to query pinned jobs - ' + callbackHelper.getErrorFromResponse(error))
        }
      }
      Loading.show()
      var queryParamArray = []
      queryParamArray['query'] = 'pinned=true'
      getDepaginatedQueryResults.getDepaginatedQueryResults('jobs/', queryParamArray, callback, globalStore.getters.apiFN)
    }
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
  },
  mounted () {
    this.refreshPage()
  }
}
</script>

<style>
</style>
