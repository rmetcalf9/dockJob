# Really a placeholder modal dialog
<template>
<q-dialog v-model="dialogVisible">
  <ExternalTriggerGoogleDriveRawClass
    v-if="jobData.ExternalTrigger.type === 'googleDriveRawClass'"
    :jobData="jobData"
    @triggerupdated="triggerupdated"
  />
  <ExternalTriggerGoogleDriveNewFileWatchClass
    v-if="jobData.ExternalTrigger.type === 'googleDriveNewFileWatchClass'"
    :jobData="jobData"
    @triggerupdated="triggerupdated"
  />
</q-dialog>
</template>

<script>
import ExternalTriggerGoogleDriveRawClass from '../../components/externalTrigger/googleDriveRawClass/view.vue'
import ExternalTriggerGoogleDriveNewFileWatchClass from '../../components/externalTrigger/googleDriveNewFileWatchClass/view.vue'

export default {
  name: 'Modal-ViewTrigger',
  props: [
    'jobData'
  ],
  components: {
    ExternalTriggerGoogleDriveRawClass,
    ExternalTriggerGoogleDriveNewFileWatchClass
  },
  data () {
    return {
      dialogVisible: false
    }
  },
  methods: {
    openViewJobTriggerDialog () {
      this.dialogVisible = true
    },
    triggerupdated () {
      this.$emit('triggerupdated')
      dialog.visible = false
    }
  }
}
</script>
