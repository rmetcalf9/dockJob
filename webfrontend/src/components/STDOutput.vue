<template>
  <div>
    <div v-for="curVal in getLineArray(val, maxLinesToShow)" :key=curVal.p @click="expandOutput">{{ curVal.v }}</div>
    <q-modal v-model="showOutputDialog" :content-css="{minWidth: '80vw', minHeight: '80vh'}">
      <q-modal-layout>
        <q-toolbar slot="header">
          <q-btn
            flat
            round
            dense
            v-close-overlay
            icon="keyboard_arrow_left"
          />
          <q-toolbar-title>
            Job Output
          </q-toolbar-title>
        </q-toolbar>
        <div class="layout-padding">
          <div v-for="curVal in getLineArray(val, undefined)" :key=curVal.p @click="expandOutput">{{ curVal.v }}</div>
        </div>
        <q-toolbar slot="footer">
          <q-toolbar-title>
            <q-btn
              color="secondary"
              :label="'Copy to Clipboard'"
              @click="copyToClipboard"
            />
          </q-toolbar-title>
        </q-toolbar>
      </q-modal-layout>
    </q-modal>

  </div>
</template>

<script>
import { Notify } from 'quasar'

// from https://stackoverflow.com/questions/400212/how-do-i-copy-to-the-clipboard-in-javascript
function fallbackCopyTextToClipboard (text) {
  var textArea = document.createElement('textarea')
  textArea.value = text
  document.body.appendChild(textArea)
  textArea.focus()
  textArea.select()

  try {
    var successful = document.execCommand('copy')
    var msg = successful ? 'successful' : 'unsuccessful'
    console.log('Fallback: Copying text command was ' + msg)
  } catch (err) {
    Notify.create('Fallback: Oops, unable to copy' + err)
  }

  document.body.removeChild(textArea)
}
function copyTextToClipboard (text) {
  if (!navigator.clipboard) {
    fallbackCopyTextToClipboard(text)
    return
  }
  navigator.clipboard.writeText(text).then(function () {
    Notify.create({color: 'positive', detail: 'Async: Copying to clipboard was successful!'})
  }, function (err) {
    Notify.create('Async: Could not copy text: ' + err)
  })
}

export default {
  props: [
    'val',
    'maxLinesToShow'
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
      },
      showOutputDialog: false
    }
  },
  methods: {
    expandOutput () {
      this.showOutputDialog = true
    },
    copyToClipboard () {
      copyTextToClipboard(this.val)
    }
  },
  computed: {
  }
}
</script>

<style>
</style>
