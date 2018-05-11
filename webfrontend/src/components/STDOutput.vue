<template>
  <div>
    <div v-for="curVal in getLineArray(val, 3)" :key=curVal.p>{{ curVal.v }}</div>
  </div>
</template>

<script>

export default {
  props: [
    'val'
  ],
  data () {
    return {
      // Function will return an array of lines. If there is more than the max it will add a '...' as the last line
      getLineArray: function (str, maxNumOfLinesToShow) {
        if (typeof (str) === 'undefined') return undefined
        var c = 0
        var lines = str.split('\n').map(function (v) { return { p: ++c, v: v } })
        if (lines.length > maxNumOfLinesToShow) {
          lines = lines.filter(function (v) {
            return v.p <= maxNumOfLinesToShow
          })
          lines = lines.concat([{ p: ++c, v: '...' }])
        }
        return lines
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
