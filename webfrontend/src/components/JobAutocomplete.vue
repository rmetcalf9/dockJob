<template>
  <div>
    <q-input
      v-model="jobName"
      type="text"
      :float-label="floatlabel"
      :error-label="errorlabel"
      :error="invalid"
    />
  </div>
</template>

<script>

export default {
  props: [
    'model',
    'floatlabel',
    'errorlabel'
  ],
  data: function () {
    return {
    }
  },
  methods: {
    setValue (jobNAME) {
      this.$emit('modelupdate', {guid: 'TODO work out guid for job ' + jobNAME, name: jobNAME})
    }
  },
  computed: {
    jobName: {
      get () {
        return this.model.name
      },
      set (val) {
        this.setValue(val)
      }
    },
    invalid () {
      return false
    }
  }
}

</script>
