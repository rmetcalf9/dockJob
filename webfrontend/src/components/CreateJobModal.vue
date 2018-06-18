<template>
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
          {{ displayValues.dialogTitle }}
        </q-toolbar-title>
      </q-toolbar>

      <q-toolbar slot="footer">
        <q-toolbar-title>
        </q-toolbar-title>
      </q-toolbar>

      <div class="layout-padding">
        <q-field helper="Name of Job" label="Job Name" :label-width="3" error-label="Job name must have more than two characters">
          <q-input v-model="showCreateJobDialogData.jobname" :error='createJobInValidJobName' />
        </q-field>
        <q-field helper="Command to execute" label="Command" :label-width="3" error-label="Command to run must be supplied">
          <q-input v-model="showCreateJobDialogData.command" type="textarea" :error='showCreateJobDialogData.command.length <= 2' />
        </q-field>
        <q-field helper="" label="Pinned to Dashboard" :label-width="3">
          <q-toggle v-model="showCreateJobDialogData.pinned" />
        </q-field>
        <q-field helper="" label="State Change Success Job" :label-width="3">
          <q-input v-model="showCreateJobDialogData.StateChangeSuccessJobGUID" type="text" float-label="Job to call when State changes to Success"
            error-label="Error"
            :error="createJobInValidStateChangeSuccessJobGUID"
          />
          TEST_START
          <JobAutocomplete
            :model="showCreateJobDialogData.StateChangeSuccessJobModel"
            floatlabel="Job to call when State changes to Success"
            errorlabel="Error"
            @modelupdate="showCreateJobDialogData.StateChangeSuccessJobModel = $event"
          />
          TEST_END
          {{ showCreateJobDialogData.StateChangeSuccessJobModel }}
          <q-input v-model="showCreateJobDialogData.StateChangeSuccessJobModel.name" type="text" />
          DEBUGEND
        </q-field>
        <q-field helper="" label="State Change Fail Job" :label-width="3">
          <q-input v-model="showCreateJobDialogData.StateChangeFailJobGUID" type="text" float-label="Job to call when State changes to Fail"
            error-label="Error"
            :error="createJobInValidStateChangeFailJobGUID"
          />
        </q-field>
        <q-field helper="" label="State Change Unknown Job" :label-width="3">
          <q-input v-model="showCreateJobDialogData.StateChangeUnknownJobGUID" type="text" float-label="Job to call when State changes to Unknown"
            error-label="Error"
            :error="createJobInValidStateChangeUnknownJobGUID"
          />
        </q-field>
        <q-field helper="" label="Unknown Timeout Override" :label-width="3">
          <q-input v-model="showCreateJobDialogData.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown" type="number" float-label="Minutes to wait before setting status to unknown (if Job hasn't been executed)"
            error-label="Error"
            :error="createJobInValidOverrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown"
          />
        </q-field>
        <q-field helper="Automatic Schedule Enabled" label="Automatic Schedule Enabled" :label-width="3">
          <q-toggle v-model="showCreateJobDialogData.enabled" />
        </q-field>
        <q-field label="Repetition Interval" :label-width="3" v-if="showCreateJobDialogData.enabled">
          <q-select
            v-model="showCreateJobDialogData.repetitionInterval.mode"
           :options="showCreateJobDialogData.repetitionInterval.modeOptions"
           :disable="!showCreateJobDialogData.enabled"
            v-if="showCreateJobDialogData.enabled"
          />
          <q-input v-model="showCreateJobDialogData.repetitionInterval.hour" type="number" float-label="Hour (24 hour format)"
            error-label="Hour must be a number between 0 and 23"
            :error="createJobInValidRepHour"
            :disable="createJobHourDisabled"
            v-if="!createJobHourDisabled"
          />
          <q-input v-model="showCreateJobDialogData.repetitionInterval.minute" type="number" float-label="Minute" error-label="Minute must be a number between 0 and 59"
            :error="createJobInValidRepMinute"
            :disable="createJobMinuteDisabled"
            v-if="!createJobMinuteDisabled"
          />
          <q-input v-model="showCreateJobDialogData.repetitionInterval.hourlyMinuteString" type="text" float-label="Comma seperates list of Minutes past hour to run" error-label="Comma seperated list of minutes past hour to run job (0-59)"
            :error="createJobInValidRepHourlyMinuteString"
            :disable="createJobHourlyMinuteStringDisabled"
            v-if="!createJobHourlyMinuteStringDisabled"
          />
          <q-select
            toggle
            multiple
            v-model="showCreateJobDialogData.repetitionInterval.days"
            :options="showCreateJobDialogData.repetitionInterval.dayOptions"
            :error="createJobInValidDays"
            :disable="createJobDaysDisabled"
            v-if="!createJobDaysDisabled"
            float-label="Day(s) of week"
            error-label="Minute must be a number between 0 and 59"
          />
          <q-input v-model="showCreateJobDialogData.repetitionInterval.dayofmonth" type="text" float-label="Comma seperates list of day of months to run" error-label="Comma seperated list of days of monyh to run job (1-31)"
            :error="createJobInValidDayOfMonth"
            :disable="createJobDOMDisabled"
            v-if="!createJobDOMDisabled"
          />
          <q-input
            v-model="showCreateJobDialogData.repetitionInterval.timezone"
            float-label="Timezone"
            :disable="createJobTimezoneDisabled"
            v-if="!createJobTimezoneDisabled"
            :error="createJobInValidTimezone"
          />
        </q-field>

        <q-btn
          color="primary"
          :label="displayValues.okButtonText"
          :disable="!createJobValidAll"
          @click="createJobMethod"
        />
        <q-btn
          v-close-overlay
          label="Cancel"
        />
      </div>
    </q-modal-layout>
  </q-modal>
</template>

<script>
import globalStore from '../store/globalStore'
import { Notify } from 'quasar'
import callbackHelper from '../callbackHelper'
import JobAutocomplete from '../components/JobAutocomplete'

function initShowCreateJobDialogData () {
  return {
    jobname: '',
    command: '',
    pinned: false,
    StateChangeSuccessJobGUID: '',
    StateChangeFailJobGUID: '',
    StateChangeUnknownJobGUID: '',
    StateChangeSuccessJobModel: {
      guid: 'tggg',
      name: 'tnnn'
    },

    overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown: 0,
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
      hourlyMinuteString: '15,45',
      hour: 1,
      days: [],
      dayOptions: [
        {
          label: 'Monday',
          value: 0
        },
        {
          label: 'Tuesday',
          value: 1
        },
        {
          label: 'Wednesday',
          value: 2
        },
        {
          label: 'Thursday',
          value: 3
        },
        {
          label: 'Friday',
          value: 4
        },
        {
          label: 'Saturday',
          value: 5
        },
        {
          label: 'Sunday',
          value: 6
        }
      ],
      timezone: globalStore.getters.serverInfo.Server.DefaultUserTimezone,
      dayofmonth: '1,15'
    }
  }
}

function commaSeperatedIntListIsInvalid (listStr, minVal, maxVal) {
  if (listStr.match('[^().0-9,]')) {
    return true
  }
  if (listStr.substr(0, 1) === ',') {
    return true
  }
  if (listStr.substr(-1) === ',') {
    return true
  }
  var invalidVals = listStr.split(',').filter(function (val) {
    var i = parseInt(val)
    if (isNaN(i)) return true
    if (i < minVal) return true
    if (i > maxVal) return true
    return false
  })
  if (invalidVals.length !== 0) {
    return true
  }
  return false
}

function pad (num, size) {
  var s = String(num)
  while (s.length < (size || 2)) { s = '0' + s }
  return s
}

function getRepIntervalString (dialogData) {
  // Even if it is disabled still output the RI string
  // if (!dialogData.enabled) return ''

  if (dialogData.repetitionInterval.mode === 'HOURLY') {
    return 'HOURLY:' + dialogData.repetitionInterval.hourlyMinuteString.trim()
  }
  if (dialogData.repetitionInterval.mode === 'MONTHLY') {
    // MONTHLY hour minute day
    return 'MONTHLY:' + pad(dialogData.repetitionInterval.minute, 2) + ':' + pad(dialogData.repetitionInterval.hour, 2) + ':' + pad(dialogData.repetitionInterval.dayofmonth, 2) + ':' + dialogData.repetitionInterval.timezone
  }
  if (dialogData.repetitionInterval.mode === 'DAILY') {
    if (dialogData.repetitionInterval.days.length === 0) {
      return 'ERROR'
    }
    if (dialogData.repetitionInterval.timezone === '') {
      return 'ERROR'
    }
    // DAILY:1:11:+++++XX:UTC
    // (+-+-+-- Each char represents DOW mon-sun + means include day, - do not)
    var dayArr = [false, false, false, false, false, false, false]
    dialogData.repetitionInterval.days.map(function (val) {
      dayArr[val] = true
    })
    var daySTR = ''
    for (var c = 0; c < 7; c++) {
      if (dayArr[c]) {
        daySTR += '+'
      } else {
        daySTR += '-'
      }
    }
    return 'DAILY:' + pad(dialogData.repetitionInterval.minute, 2) + ':' + pad(dialogData.repetitionInterval.hour, 2) + ':' + daySTR + ':' + dialogData.repetitionInterval.timezone
  }
  return 'ERROR'
}

export default {
  components: {
    JobAutocomplete
  },
  data () {
    return {
      displayValues: {
        dialogTitle: '',
        okButtonText: '',
        sucessMessage: '',
        failMessage: ''
      },
      origJobObject: null,
      showCreateJobDialog: false,
      showCreateJobDialogData: initShowCreateJobDialogData(),
      repititionIntervalString: '',
      createdOKCallback: undefined // Function called if a new job is created
    }
  },
  methods: {
    openCreateJobDialog (confirmFunction, origJobObject = undefined) {
      // console.log('openCreateJobDialog')
      this.showCreateJobDialogData = initShowCreateJobDialogData()
      this.showCreateJobDialog = true
      this.createdOKCallback = confirmFunction
      this.origJobObject = origJobObject
      if (typeof (this.origJobObject) !== 'undefined') {
        // Edit mode
        this.displayValues = {
          dialogTitle: 'Edit Job ' + origJobObject.name,
          okButtonText: 'Update',
          sucessMessage: 'Successfully updated job ',
          failMessage: 'Failed to update job - '
        }
        this.showCreateJobDialogData.jobname = origJobObject.name
        this.showCreateJobDialogData.command = origJobObject.command
        if (typeof (origJobObject.enabled) !== 'undefined') {
          this.showCreateJobDialogData.enabled = origJobObject.enabled
        }
        this.showCreateJobDialogData.pinned = origJobObject.pinned
        if (typeof (origJobObject.StateChangeSuccessJobGUID) !== 'undefined' && origJobObject.StateChangeSuccessJobGUID !== null) {
          this.showCreateJobDialogData.StateChangeSuccessJobGUID = origJobObject.StateChangeSuccessJobGUID
        }
        if (typeof (origJobObject.StateChangeFailJobGUID) !== 'undefined' && origJobObject.StateChangeFailJobGUID !== null) {
          this.showCreateJobDialogData.StateChangeFailJobGUID = origJobObject.StateChangeFailJobGUID
        }
        if (typeof (origJobObject.StateChangeUnknownJobGUID) !== 'undefined' && origJobObject.StateChangeUnknownJobGUID !== null) {
          this.showCreateJobDialogData.StateChangeUnknownJobGUID = origJobObject.StateChangeUnknownJobGUID
        }

        if (typeof (origJobObject.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown) !== 'undefined' && origJobObject.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown !== null) {
          this.showCreateJobDialogData.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown = origJobObject.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown
        }

        if ((typeof (origJobObject.repetitionInterval) !== 'undefined') && (origJobObject.repetitionInterval !== '')) {
          var arr = []
          if (this.origJobObject.repetitionInterval.startsWith('DAILY')) {
            arr = this.origJobObject.repetitionInterval.split(':')
            this.showCreateJobDialogData.repetitionInterval.mode = 'DAILY'
            this.showCreateJobDialogData.repetitionInterval.minute = arr[1]
            this.showCreateJobDialogData.repetitionInterval.hour = arr[2]
            var dayArr = []
            for (var c = 0; c < 7; c++) {
              if (arr[3][c] === '+') {
                dayArr.push(c)
              }
            }
            this.showCreateJobDialogData.repetitionInterval.days = dayArr
            this.showCreateJobDialogData.repetitionInterval.timezone = arr[4]

            // not overriding defaults
            this.showCreateJobDialogData.repetitionInterval.dayofmonth = 1
          } else if (this.origJobObject.repetitionInterval.startsWith('MONTHLY')) {
            arr = this.origJobObject.repetitionInterval.split(':')
            this.showCreateJobDialogData.repetitionInterval.mode = 'MONTHLY'
            this.showCreateJobDialogData.repetitionInterval.minute = arr[1]
            this.showCreateJobDialogData.repetitionInterval.hour = arr[2]
            this.showCreateJobDialogData.repetitionInterval.timezone = arr[4]
            this.showCreateJobDialogData.repetitionInterval.dayofmonth = arr[3]

            // not overriding defaults
            this.showCreateJobDialogData.repetitionInterval.days = []
          } else if (this.origJobObject.repetitionInterval.startsWith('HOURLY')) {
            arr = this.origJobObject.repetitionInterval.split(':')
            this.showCreateJobDialogData.repetitionInterval.mode = 'HOURLY'
            this.showCreateJobDialogData.repetitionInterval.hourlyMinuteString = arr[1]

            // Not overriding defaults
            // this.showCreateJobDialogData.repetitionInterval.hour = 1
            // this.showCreateJobDialogData.repetitionInterval.days = []
            // this.showCreateJobDialogData.repetitionInterval.timezone = arr[4]
            // this.showCreateJobDialogData.repetitionInterval.dayofmonth = arr[3]
          } else {
            console.log('Unrecognised type - "' + origJobObject.repetitionInterval + '"')
          }
        }
      } else {
        // Create mode
        this.displayValues = {
          dialogTitle: 'Create New Job',
          okButtonText: 'Create',
          sucessMessage: 'Successfully created job ',
          failMessage: 'Failed to create job - '
        }
      }
    },
    createJobMethod () {
      if (!this.createJobValidAll) {
        Notify.create('Please review fields again.')
        return
      }
      this.repititionIntervalString = getRepIntervalString(this.showCreateJobDialogData)
      if ((this.repititionIntervalString === 'ERROR') && (this.enabled === true)) {
        Notify.create('Please review fields again. (Repitition Interval)')
        return
      }
      if (this.repititionIntervalString === 'ERROR') {
        this.repititionIntervalString = ''
      }
      this.showCreateJobDialog = false
      var TTT = this
      var callback = {
        ok: function (response) {
          if (typeof (TTT.createdOKCallback) !== 'undefined') {
            TTT.createdOKCallback(response.data)
          }
          Notify.create({color: 'positive', detail: TTT.displayValues.sucessMessage + response.data.name})
        },
        error: function (error) {
          Notify.create(TTT.displayValues.failMessage + callbackHelper.getErrorFromResponse(error))
        }
      }
      var payload = {
        'name': this.showCreateJobDialogData.jobname,
        'enabled': this.showCreateJobDialogData.enabled,
        'command': this.showCreateJobDialogData.command,
        'repetitionInterval': this.repititionIntervalString,
        'pinned': this.showCreateJobDialogData.pinned,
        'overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown': this.showCreateJobDialogData.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown
      }
      if (this.showCreateJobDialogData.StateChangeSuccessJobGUID !== '') {
        payload.StateChangeSuccessJobGUID = this.showCreateJobDialogData.StateChangeSuccessJobGUID
      }
      if (this.showCreateJobDialogData.StateChangeFailJobGUID !== '') {
        payload.StateChangeFailJobGUID = this.showCreateJobDialogData.StateChangeFailJobGUID
      }
      if (this.showCreateJobDialogData.StateChangeUnknownJobGUID !== '') {
        payload.StateChangeUnknownJobGUID = this.showCreateJobDialogData.StateChangeUnknownJobGUID
      }
      if (typeof (this.origJobObject) !== 'undefined') {
        // console.log('PUT With')
        // console.log(payload)
        globalStore.getters.apiFN('PUT', 'jobs/' + this.origJobObject.guid,
          payload,
          callback
        )
      } else {
        // console.log('POST With')
        // console.log(payload)
        globalStore.getters.apiFN('POST', 'jobs/',
          payload,
          callback
        )
      }
    }
  },
  computed: {
    createJobHourDisabled () {
      return !((this.showCreateJobDialogData.enabled) && (this.showCreateJobDialogData.repetitionInterval.mode !== 'HOURLY'))
    },
    createJobMinuteDisabled () {
      return !((this.showCreateJobDialogData.enabled) && (this.showCreateJobDialogData.repetitionInterval.mode !== 'HOURLY'))
    },
    createJobHourlyMinuteStringDisabled () {
      return !((this.showCreateJobDialogData.enabled) && (this.showCreateJobDialogData.repetitionInterval.mode === 'HOURLY'))
    },
    createJobDaysDisabled () {
      return !((this.showCreateJobDialogData.enabled) && (this.showCreateJobDialogData.repetitionInterval.mode === 'DAILY'))
    },
    createJobTimezoneDisabled () {
      return !((this.showCreateJobDialogData.enabled) && (this.showCreateJobDialogData.repetitionInterval.mode !== 'HOURLY'))
    },
    createJobDOMDisabled () {
      return !((this.showCreateJobDialogData.enabled) && (this.showCreateJobDialogData.repetitionInterval.mode === 'MONTHLY'))
    },
    // ---------------- END DISABLE -------------------
    createJobInValidJobName () {
      return this.showCreateJobDialogData.jobname.length <= 2
    },
    createJobInValidJobCommand () {
      return this.showCreateJobDialogData.command.length <= 2
    },
    createJobInValidRepMinute () {
      return (!this.createJobMinuteDisabled) && ((this.showCreateJobDialogData.repetitionInterval.minute < 0) || (this.showCreateJobDialogData.repetitionInterval.minute > 59))
    },
    createJobInValidRepHourlyMinuteString () {
      if (this.createJobHourlyMinuteStringDisabled) {
        return false
      }
      return commaSeperatedIntListIsInvalid(this.showCreateJobDialogData.repetitionInterval.hourlyMinuteString.trim(), 0, 59)
    },
    createJobInValidDayOfMonth () {
      if (this.createJobDOMDisabled) {
        return false
      }
      return commaSeperatedIntListIsInvalid(this.showCreateJobDialogData.repetitionInterval.dayofmonth.trim(), 1, 31)
    },
    createJobInValidRepHour () {
      return (!this.createJobHourDisabled) && ((this.showCreateJobDialogData.repetitionInterval.hour < 0) || (this.showCreateJobDialogData.repetitionInterval.hour > 23))
    },
    createJobInValidDays () {
      return (!this.createJobDaysDisabled) && (this.showCreateJobDialogData.repetitionInterval.days.length === 0)
    },
    createJobInValidTimezone () {
      return (!this.createJobTimezoneDisabled) && (this.showCreateJobDialogData.repetitionInterval.timezone.length === 0)
    },
    createJobInValidOverrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown () {
      return (this.showCreateJobDialogData.overrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown < 0)
    },
    createJobInValidStateChangeSuccessJobGUID () {
      return false // TODO
    },
    createJobInValidStateChangeFailJobGUID () {
      return false // TODO
    },
    createJobInValidStateChangeUnknownJobGUID () {
      return false // TODO
    },
    createJobValidAll () {
      if (this.createJobInValidJobName) return false
      if (this.createJobInValidJobCommand) return false
      if (this.createJobInValidRepMinute) return false
      if (this.createJobInValidRepHour) return false
      if (this.createJobInValidDays) return false
      if (this.createJobInValidTimezone) return false
      if (this.createJobInValidRepHourlyMinuteString) return false
      if (this.createJobInValidDayOfMonth) return false
      if (this.createJobInValidOverrideMinutesBeforeMostRecentCompletionStatusBecomesUnknown) return false
      if (this.createJobInValidStateChangeSuccessJobGUID) return false
      if (this.createJobInValidStateChangeFailJobGUID) return false
      if (this.createJobInValidStateChangeUnknownJobGUID) return false
      return true
    }
  }
}
</script>

<style>
</style>
