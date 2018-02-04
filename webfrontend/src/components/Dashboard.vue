<template>
  <div class="layout-padding card-examples row items-start">
    <q-card inline>
      <q-card-title>
        Server Info
        <span slot="subtitle">Basic Server Information</span>
      </q-card-title>
      <q-card-main>
        Total jobs setup, Number Scheduled, Number Manual
      </q-card-main>
    </q-card>

    <q-card inline>
      <q-card-title>
        Next Run
        <span slot="subtitle">Next Job due to run</span>
      </q-card-title>
      <q-card-main>
        Job Name, Date Time, How Long
      </q-card-main>
    </q-card>

    <q-card inline>
      <q-card-title>
        Job Logs
        <span slot="subtitle">Job results</span>
      </q-card-title>
      <q-card-main>
        Sucessfully completed, Errored
      </q-card-main>
    </q-card>

  </div>
</template>

<script>
import {
  QCard,
  QCardTitle,
  QCardMain
} from 'quasar'

export default {
  components: {
    QCard,
    QCardTitle,
    QCardMain
  },
  data () {
    return {
    }
  },
  computed: {
  }
}
</script>

<style>
</style>
