# Really a placeholder modal dialog
<template>
<q-dialog v-model="dialogVisible">
  <ExternalTriggerGoogleDriveRawClass
    v-if="jobData.ExternalTrigger.type === 'googleDriveRawClass'"
    :jobData="jobData"
    @triggerupdated="triggerupdated"
    @deactivateendpoint="deactivateendpoint"
  />
  <ExternalTriggerGoogleDriveNewFileWatchClass
    v-if="jobData.ExternalTrigger.type === 'googleDriveNewFileWatchClass'"
    :jobData="jobData"
    @triggerupdated="triggerupdated"
    @deactivateendpoint="deactivateendpoint"
  />
</q-dialog>
</template>

<script>
import ExternalTriggerGoogleDriveRawClass from '../../components/externalTrigger/googleDriveRawClass/view.vue'
import ExternalTriggerGoogleDriveNewFileWatchClass from '../../components/externalTrigger/googleDriveNewFileWatchClass/view.vue'

import { Notify } from 'quasar'

import callDockjobBackendApi from '../../callDockjobBackendApi'
import callbackHelper from '../../callbackHelper'

import { useLoginStateStore } from 'stores/loginState'
import { useServerStaticStateStore } from 'stores/serverStaticState'

export default {
  name: 'Modal-ViewTrigger',
  props: [
    'jobData'
  ],
  components: {
    ExternalTriggerGoogleDriveRawClass,
    ExternalTriggerGoogleDriveNewFileWatchClass
  },
  setup () {
    const loginStateStore = useLoginStateStore()
    const serverStaticStateStore = useServerStaticStateStore()
    return { loginStateStore, serverStaticStateStore }
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
      dialog.visible = false
    },
    deactivateendpoint () {
      const TTT = this
      const callback = {
        ok: function (response) {
          Notify.create({color: 'positive', message: 'Trigger removed'})
          TTT.$emit('triggerupdated')
          dialog.visible = false
        },
        error: function (error) {
          Notify.create({color: 'negative', message: 'Failed to remove trigger endpoint - ' + callbackHelper.getErrorFromResponse(error)})
        }
      }
      const wrappedCallApiFn = callDockjobBackendApi.getWrappedCallApi({
        loginStateStore: TTT.loginStateStore,
        apiurl: TTT.serverStaticStateStore.staticServerInfo.data.apiurl
      })
      const postdata = {}
      wrappedCallApiFn({
        method: 'POST',
        path:  '/jobs/' + TTT.jobData.guid + '/deactivateTrigger',
        postdata: postdata,
        callback: callback
      })
    }
  }
}
</script>
