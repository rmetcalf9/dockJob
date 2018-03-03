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

        <q-btn
          color="primary"
          v-close-overlay
          label="Close"
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
      minute: 0,
      hour: 0,
      days: {
        mon: false,
        tue: false,
        wed: false,
        thur: false,
        fri: false,
        sat: false,
        sun: false
      },
      timezone: 'TODO'
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
