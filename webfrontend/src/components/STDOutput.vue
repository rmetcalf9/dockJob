<template>
  <div>
    <div v-for="curVal in outputValArr" :key=curVal.p>{{ curVal.v }}</div>
  </div>
</template>

<script>

export default {
  props: [
    'val'
  ],
  data () {
    return {
    }
  },
  methods: {
  },
  computed: {
    outputValArr () {
      var c = 0
      return this.val.split('\n').map(function (v) { return { p: ++c, v: v } })
    }
  }
}
</script>

<style>
</style>
