// https://vuejs.org/v2/guide/components.html
// Get thie component recieving and emmitting properly
<template>
  <q-select
    ref="sel"
    multiple
    outlined
    :options="localTableVisibleColumns"
    v-model="internal_model"
    @update:model-value="change"
  >
    <template v-slot:selected>
      Show {{ internal_model.length }} fields
    </template>
  </q-select>
</template>

<script>

export default {
  props: [
    'valuex',
    'columns'
  ],
  data () {
    return {
      localTableVisibleColumns: [],
      internal_model: []
    }
  },
  methods: {
    change (event) {
      this.$emit('update:valuex', this.internal_model.map(function (x) {
        return x.value
      }))
      this.$refs.sel.hidePopup()
    }
  },
  computed: {
  },
  mounted: function () {
    const TTT=this
    this.localTableVisibleColumns = this.columns.filter(function (x) { return !x.required }).map(function (x) {
      return {
        value: x.name,
        label: x.label,
        disable: x.required
      }
    })
    const init_mod = this.valuex.map(function (x) {
      return {
        value: x,
        label: TTT.localTableVisibleColumns.filter(function (y) {
          return y.value === x
        }).map(function (z) {
          return z.label
        }),
        disable: false
      }
    })
    this.internal_model = init_mod
  }
}
</script>[

<style>
</style>
