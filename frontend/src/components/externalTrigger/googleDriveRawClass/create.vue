<template>
    <div>
      <p>Activate a Raw google trigger on this Job. This will create an endpoint which will allow this process to be triggerd via google notification API.</p>
      <a href="https://developers.google.com/drive/api/guides/push" target=_new>Google notification API documentation</a>
      <br>
      <br>
      <q-btn
        color="primary"
        label="Click here to activate endpoint"
        @click="activateEndpoint"
      />

    </div>
</template>

<script>
import { Notify } from 'quasar'

import callDockjobBackendApi from '../../../callDockjobBackendApi'
import callbackHelper from '../../../callbackHelper'

import { useLoginStateStore } from 'stores/loginState'
import { useServerStaticStateStore } from 'stores/serverStaticState'


export default {
  name: 'Comp-ExternalTrigger-GoogleDriveRawClass-Create',
  props: [
    'jobData'
  ],
  components: {
  },
  setup () {
    const loginStateStore = useLoginStateStore()
    const serverStaticStateStore = useServerStaticStateStore()
    return { loginStateStore, serverStaticStateStore }
  },
  data () {
    return {
    }
  },
  methods: {
    activateEndpoint () {
      const TTT = this
      const callback = {
        ok: function (response) {
          Notify.create({color: 'positive', message: 'Trigger created'})
          TTT.$emit('triggercreated')
        },
        error: function (error) {
          Notify.create({color: 'negative', message: 'Failed to activate endpoint - ' + callbackHelper.getErrorFromResponse(error)})
        }
      }
      const wrappedCallApiFn = callDockjobBackendApi.getWrappedCallApi({
        loginStateStore: TTT.loginStateStore,
        apiurl: TTT.serverStaticStateStore.staticServerInfo.data.apiurl
      })
      const postdata = {
        triggerType: 'googleDriveRawClass',
        triggerOptions: {}
      }
      wrappedCallApiFn({
        method: 'POST',
        path:  '/jobs/' + TTT.jobData.guid + '/activateTrigger',
        postdata: postdata,
        callback: callback
      })
    }
  },
  computed: {
  },
  mounted () {
  }
}

</script>
