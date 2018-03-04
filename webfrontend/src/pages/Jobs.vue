<template>
  <div>
    <q-btn
      color="primary"
      push
      @click="openCreateJobDialog"
    >Create Job</q-btn>
    <q-table
      title='Jobs'
      :data="jobData"
      :columns="jobTableColumns"
      :filter="filter"
    >
    <template slot="top-left" slot-scope="props">
    </template>
  </q-table>

  <q-modal v-model="showCreateJobDialog" :content-css="{minWidth: '80vw', minHeight: '80vh'}">
    <q-modal-layout>
      <q-toolbar slot="header">
        <q-btn
          flat
          round
          dense
          v-close-overlay
          icon="keyboard_arrow_left"
        />
        <q-toolbar-title>
          Create New Job
        </q-toolbar-title>
      </q-toolbar>

      <q-toolbar slot="footer">
        <q-toolbar-title>
        </q-toolbar-title>
      </q-toolbar>

      <div class="layout-padding">
        <q-field helper="Name of Job" label="Job name" :label-width="3">
          <q-input v-model="showCreateJobDialogData.jobname" />
        </q-field>
        <q-field helper="Command to execute" label="Command" :label-width="3">
          <q-input v-model="showCreateJobDialogData.command" type="textarea" />
        </q-field>
        <q-field helper="Automatic Schedule Enabled" label="Automatic Schedule Enabled" :label-width="3">
          <q-toggle v-model="showCreateJobDialogData.enabled" />
        </q-field>
        <q-field label="Repetition Interval" :label-width="3">
          <q-select
            v-model="showCreateJobDialogData.repetitionInterval.mode"
           :options="showCreateJobDialogData.repetitionInterval.modeOptions"
           :disable="!showCreateJobDialogData.enabled"
          />
          <q-input v-model="showCreateJobDialogData.repetitionInterval.hour" type="number" float-label="Hour (24 hour format)"
            :disable="!((showCreateJobDialogData.enabled) && (showCreateJobDialogData.repetitionInterval.mode !== 'HOURLY'))"
          />
          <q-input v-model="showCreateJobDialogData.repetitionInterval.minute" type="number" float-label="Minute"
            :disable="!showCreateJobDialogData.enabled"
          />
          <q-select
            toggle
            multiple
            v-model="showCreateJobDialogData.repetitionInterval.days"
           :options="showCreateJobDialogData.repetitionInterval.dayOptions"
            :disable="!((showCreateJobDialogData.enabled) && (showCreateJobDialogData.repetitionInterval.mode === 'DAILY'))"
            float-label="Day(s) of week"
          />
          <q-input v-model="showCreateJobDialogData.repetitionInterval.dayofmonth" type="number" float-label="Day of Month"
            :disable="!((showCreateJobDialogData.enabled) && (showCreateJobDialogData.repetitionInterval.mode === 'MONTHLY'))"
          />
          <q-input v-model="showCreateJobDialogData.repetitionInterval.timezone" float-label="Timezone" :disable="!showCreateJobDialogData.enabled" />
        </q-field>

        <q-btn
          color="primary"
          v-close-overlay
          label="Create"
        />
        <q-btn
          v-close-overlay
          label="Cancel"
        />
      </div>
    </q-modal-layout>
  </q-modal>
  </div>

</template>

<script>
import globalStore from '../store/globalStore'

function initShowCreateJobDialogData () {
  return {
    jobname: '',
    command: '',
    enabled: true,
    repetitionInterval: {
      mode: 'DAILY', // Monthly, Daily, Hourly
      modeOptions: [
        {
          label: 'Daily',
          value: 'DAILY'
        },
        {
          label: 'Monthly',
          value: 'MONTHLY'
        },
        {
          label: 'Hourly',
          value: 'HOURLY'
        }
      ],
      minute: 1,
      hour: 1,
      days: [],
      dayOptions: [
        {
          label: 'Monday',
          value: 'MON'
        },
        {
          label: 'Tuesday',
          value: 'TUE'
        },
        {
          label: 'Wednesday',
          value: 'WED'
        },
        {
          label: 'Thursday',
          value: 'THUR'
        },
        {
          label: 'Friday',
          value: 'FRI'
        },
        {
          label: 'Saturday',
          value: 'SAT'
        },
        {
          label: 'Sunday',
          value: 'SUN'
        }
      ],
      timezone: globalStore.getters.serverInfo.Server.DefaultUserTimezone,
      dayofmonth: 1
    }
  }
}

export default {
  data () {
    return {
      showCreateJobDialog: false,
      showCreateJobDialogData: initShowCreateJobDialogData(),
      jobTableColumns: [
        {
          name: 'name',
          required: true,
          label: 'Job Name',
          align: 'left',
          field: 'name',
          sortable: true,
          filter: true
        }
      ],
      jobData: [
        {
          name: 'TODO'
        },
        {
          name: 'ANOther'
        }
      ],
      filter: ''
    }
  },
  methods: {
    openCreateJobDialog () {
      this.showCreateJobDialogData = initShowCreateJobDialogData()
      this.showCreateJobDialog = true
    }
  },
  computed: {
    datastoreState () {
      return globalStore.getters.datastoreState
    }
  }
}
</script>

<style>
</style>
