<template>
  <div>
    <div>
      <div class="full-width column wrap items-center content-center">
        <div>Trigger on new files in Google drive</div>
        <div style="width: 300px;">
          <q-input
            v-model="folder_path"
             helper="Folder path without trailing slash"
             label="Folder Path"
             :label-width="3"
          />
        </div>
        <div>Click here to authorising with google and create the trigger</div>
        <div>
          <q-btn
            @click="autoriseWithGoogle"
            color="primary"
            label="Auth with google"
            class = "float-right q-ml-xs"
          ></q-btn>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Loading } from 'quasar'
import { Notify } from 'quasar'

import callDockjobBackendApi from '../../../callDockjobBackendApi'
import callbackHelper from '../../../callbackHelper'

import { useLoginStateStore } from 'stores/loginState'
import { useServerStaticStateStore } from 'stores/serverStaticState'


export default {
  name: 'Comp-ExternalTrigger-GoogleDriveFileWatchClass-Create',
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
      folder_path: '/Projects/Property/Business Cards'
    }
  },
  methods: {
    tododel () {
      this.$emit('triggercreated')
    },
    autoriseWithGoogle () {
      const TTT = this
      Loading.show()
      const client = window.google.accounts.oauth2.initTokenClient({
        client_id: '425120641293-lg3p5p4n5g3vrk0soe77n35md9k0tt98.apps.googleusercontent.com',
        scope: 'https://www.googleapis.com/auth/drive.metadata.readonly',
        ux_mode: 'popup',
        callback: (tokenResponse) => {
          Loading.hide()
          TTT.createTrigger(tokenResponse.access_token)
        }
      })
      client.requestAccessToken()
    },
    createTrigger (access_token) {
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
      console.log('GGG', access_token)
      const postdata = {
        triggerType: 'googleDriveNewFileWatchClass',
        triggerOptions: {
          access_token,
          folder_path: TTT.folder_path
        }
      }
      console.log('postdata', postdata)
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
