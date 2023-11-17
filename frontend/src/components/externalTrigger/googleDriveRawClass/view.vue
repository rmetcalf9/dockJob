<template>
  <q-layout view="Lhh lpR fff" container class="bg-white" style="width: 700px; max-width: 80vw;">
    <q-header class="bg-primary">
      <q-toolbar>
        <q-toolbar-title>
          Google Dirve Raw Trigger
        </q-toolbar-title>
        <q-btn flat v-close-popup round dense icon="close" />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page padding class="column wrap justify-center items-center content-center q-gutter-lg">
        <div>This process can be triggered by the google notification API.</div>
        <div>{{ curlCommand }}</div>
        <q-btn
          color="secondary"
          :label="'Copy to Clipboard'"
          @click="copyToClipboard"
        />
        <div>
          <q-btn
            color="primary"
            label="Deactivate endpoint"
            @click="$emit('deactivateendpoint')"
          />
        </div>
      </q-page>
    </q-page-container>

    <q-footer class="bg-black text-white">
      <q-toolbar inset>
        <q-btn
          v-close-popup
          label="Cancel"
        />
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script>
import { Notify } from 'quasar'

import { useServerStaticStateStore } from 'stores/serverStaticState'

// from https://stackoverflow.com/questions/400212/how-do-i-copy-to-the-clipboard-in-javascript
function fallbackCopyTextToClipboard (text) {
  var textArea = document.createElement('textarea')
  textArea.value = text
  document.body.appendChild(textArea)
  textArea.focus()
  textArea.select()

  try {
    var successful = document.execCommand('copy')
    var msg = successful ? 'successful' : 'unsuccessful'
    console.log('Fallback: Copying text command was ' + msg)
  } catch (err) {
    Notify.create('Fallback: :( Oops, unable to copy' + err)
  }

  document.body.removeChild(textArea)
}
function copyTextToClipboard (text) {
  if (!navigator.clipboard) {
    fallbackCopyTextToClipboard(text)
    return
  }
  navigator.clipboard.writeText(text).then(function () {
    Notify.create({color: 'positive', message: 'Async: Copying to clipboard was successful!'})
  }, function (err) {
    Notify.create('Async: Could not copy text: ' + err)
  })
}

export default {
  name: 'Comp-ExternalTrigger-GoogleDriveRawClass-View',
  props: [
    'jobData'
  ],
  components: {
  },
  setup () {
    const serverStaticStateStore = useServerStaticStateStore()
    return { serverStaticStateStore }
  },
  methods: {
    copyToClipboard () {
      copyTextToClipboard(this.curlCommand)
      Notify.create({color: 'positive', message: 'Curl command coppied to clipboard'})
    }
  },
  computed: {
    curlCommand () {
      const host = this.serverStaticStateStore.staticServerInfo.data.apiurl.replace('/api','/triggerapi')
      // http://superego:8098/triggerapi/trigger/
      return 'curl -X POST ' + host + '/trigger/' + this.jobData.ExternalTrigger.urlpasscode + ' -H "X-Goog-Channel-ID: ' + this.jobData.ExternalTrigger.nonurlpasscode + '" -H "X-Goog-Channel-Token: ' + this.jobData.ExternalTrigger.encodedjobguid + '"'
    }
  }
}
</script>
