<template>
<q-layout view="Lhh lpR fff" container class="bg-white" style="width: 700px; max-width: 80vw;">
  <q-header class="bg-primary">
    <q-toolbar>
      <q-toolbar-title>
        Google Driver new Watch Trigger
      </q-toolbar-title>
      <q-btn flat v-close-popup round dense icon="close" />
    </q-toolbar>
  </q-header>

  <q-page-container>
    <q-page padding class="column wrap justify-center items-center content-center q-gutter-lg">
      <div>This process triggers from a google notification</div>
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
import { useServerInfoWithDerivedStore } from 'stores/serverInfoWithDerived'

export default {
  name: 'Comp-ExternalTrigger-GoogleDriveNewFileWatchClass-View',
  props: [
    'jobData'
  ],
  components: {
  },
  setup () {
  },
  methods: {
  },
  computed: {
  }  
}
</script>
