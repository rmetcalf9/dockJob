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
      <q-page padding>
        <div>This process can be triggered by the google notification API.</div>
        <div>{{ curlCommand }}</div>
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

export default {
  name: 'Comp-ExternalTrigger-GoogleDriveRawClass-View',
  props: [
    'jobData'
  ],
  components: {
  },
  methods: {
  },
  computed: {
    curlCommand () {
      return 'curl -X POST http://superego:8098/triggerapi/trigger/' + this.jobData.ExternalTrigger.urlpasscode + ' -H "X-Goog-Channel-ID: ' + this.jobData.ExternalTrigger.nonurlpasscode + '" -H "X-Goog-Channel-Token: ' + this.jobData.ExternalTrigger.encodedjobguid + '"'
    }
  }
}
</script>
