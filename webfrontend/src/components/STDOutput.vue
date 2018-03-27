<template>
  <div>
    <div v-for="curVal in getLineArray(val)" :key=curVal.p>{{ curVal.v }}</div>
  </div>
</template>

<script>

export default {
  props: [
    'val'
  ],
  data () {
    return {
      getLineArray: function (str) {
        if (typeof (str) === 'undefined') return undefined
        var c = 0
        return str.split('\n').map(function (v) { return { p: ++c, v: v } })
      }
    }
  },
  methods: {
  },
  computed: {
  }
}
</script>

<style>
</style>
