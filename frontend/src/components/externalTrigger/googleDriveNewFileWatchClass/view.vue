<template>
  <q-layout view="Lhh lpR fff" container class="bg-white" style="width: 700px; max-width: 80vw;">
    <q-header class="bg-primary">
      <q-toolbar>
        <q-toolbar-title>
          View Trigger TODO
        </q-toolbar-title>
        <q-btn flat v-close-popup round dense icon="close" />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page padding>
        TEST VIEW
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
  name: 'Comp-ExternalTrigger-GoogleDriveNewFileWatchClass-View',
  props: [
    'jobData'
  ]
}
</script>
