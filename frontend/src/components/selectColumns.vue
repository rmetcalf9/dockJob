// https://vuejs.org/v2/guide/components.html
// Get thie component recieving and emmitting properly
<template>
  <q-select
    multiple outlined
    hide-selected
    :options="columnsForEnableDropdown"
    label="Fields:"
    style="width: 300px"
    v-bind:value="localTableVisibleColumns"
    v-on:input="updateTableVisibleColumns"
    :display-value="''"
  >
    <template v-slot:selected-item>
    </template>
  </q-select>
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
    // I think this is what Emit-value does
    updateTableVisibleColumns (event) {
      this.localTableVisibleColumns = event
      this.$emit('input', this.localTableVisibleColumns.map(function (x) {
        return x.value
      }))
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
  },
  mounted: function () {
    var a = this.columnsForEnableDropdown
    function findCol (name) {
      return a.filter(function (x) {
        return x.value === name
      })
    }
    this.localTableVisibleColumns = this.value.map(function (x) {
      var col = findCol(x)
      if (col.length === 0) {
        // columns are not loaded yet
        return {
          value: x,
          label: x,
          disable: false
        }
      }
      return {
        value: x,
        label: col[0].label,
        disable: col[0].required
      }
    }).filter(function (x) {
      return !x.disable
    })
  }
}
</script>[

<style>
</style>
