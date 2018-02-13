<template>
  <div class="error-page window-height window-width bg-light column items-center no-wrap">
    <div class="error-code bg-primary flex items-center content-center justify-center">
      Login
    </div>
    <div>
      <div class="error-card shadow-4 bg-white column items-center justify-center no-wrap">
        <q-tabs align="justify" v-if="numTabsVisible > 0">
          <q-tab name="usernamePass" slot="title"label="User Details" v-if="tabs.usernamePass"/>
          <q-tab name="xxx" slot="title" label="XXX" v-if="tabs.xxx"/>

          <q-tab-pane name="usernamePass">
            Username pass icons TODO tab
            <p class="text-center group">
              <q-btn
                color="primary"
                push
                @click="usernamePassLogin"
              >
                Login
              </q-btn>
            </p>
          </q-tab-pane>
          <q-tab-pane name="xxx">TODO Next Tab</q-tab-pane>
        </q-tabs>

      </div>
    </div>
  </div>
</template>

<script>
import {
  QBtn,
  QIcon,
  QTabs,
  QTab,
  QTabPane,
  Loading,
  Toast
} from 'quasar'
import globalStore from '../stores/globalStore'

export default {
  components: {
    QBtn,
    QIcon,
    QTabs,
    QTab,
    QTabPane
  },
  data () {
    return {
      tabs: {
        usernamePass: false,
        xxx: false
      }
    }
  },
  computed: {
    numTabsVisible () {
      var a = 0
      for (var k in this.tabs) {
        if (this.tabs.hasOwnProperty(k)) {
          if (this.tabs[k]) {
            a++
          }
        }
      }
      return a
    }
  },
  methods: {
    creationHandler () {
      var TTT = this
      if (globalStore.getters.datastoreState === 'INITIAL') {
        Loading.show()
        var callback = {
          ok: function (response) {
            Loading.hide()
            if (globalStore.getters.datastoreState === 'INITIAL') {
              console.log('Error state STILL initial - stopping infinite loop')
            }
            else {
              // TTT.$router.replace(TTT.$route.query.redirect || '/')
              TTT.creationHandler()
            }
          },
          error: function (response) {
            Loading.hide()
            console.log('Error frontend connection data state: ' + response.message)
            Toast.create(response.message)
          }
        }
        globalStore.dispatch('init', {callback: callback})
        return
      }
      if (globalStore.getters.datastoreState === 'REQUIRE_LOGIN') {
        this.tabs.usernamePass = false
        this.tabs.xxx = false
        console.log(globalStore.getters.connectionData.apiaccesssecurity)
        for (var i = 0; i < globalStore.getters.connectionData.apiaccesssecurity.length; i++) {
          var curAuthMethod = globalStore.getters.connectionData.apiaccesssecurity[i]
          if (curAuthMethod.type === 'basic-auth') this.tabs.usernamePass = true
        }
        return
      }
      Toast.create('Invalid state ' + globalStore.getters.datastoreState)
      console.log('TODO deal with state ' + globalStore.getters.datastoreState)
    },
    usernamePassLogin () {
      console.log('TODO')
    }
  },
  created () {
    this.creationHandler()
  }
}
</script>

<style lang="stylus">
.error-page
  .error-code
    height 50vh
    width 100%
    padding-top 15vh
    @media (orientation: landscape) { 
      font-size 30vw
    }
    @media (orientation: portrait) { 
      font-size 30vh
    }
    color rgba(255, 255, 255, .2)
    overflow hidden
  .error-card
    border-radius 2px
    margin-top -50px
    width 80vw
    max-width 600px
    padding 25px
    > i
      font-size 5rem
</style>
