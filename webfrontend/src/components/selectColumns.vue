<template>
  // https://vuejs.org/v2/guide/components.html
  // TODO Get thie component recieving and emmitting properly
  <q-select
    v-model="localTableVisibleColumns"
    multiple outlined
    :options="columnsForEnableDropdown"
    label="Fields:"
    style="width: 300px"
    v-on:input="updateTableVisibleColumns"
  />
</template>

<script>

export default {
  props: [
    'value',
    'columns'
  ],
  data () {
    return {
      localTableVisibleColumns: []
    }
  },
  methods: {
    updateTableVisibleColumns (event) {
      this.model = this.localTableVisibleColumns.map(function (x) {
        return x.value
      })
      console.log('EVENT:', event)
      this.$emit('input', this.value)
    }
  },
  computed: {
    columnsForEnableDropdown () {
      return this.columns.filter(function (x) { return !x.required }).map(function (x) {
        return {
          value: x.name,
          label: x.label,
          disable: x.required
        }
      })
    }
  }
}
</script>

<style>
</style>
