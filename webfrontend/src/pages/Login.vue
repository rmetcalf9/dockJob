<template>
  <div class="error-page window-height window-width bg-light column items-center no-wrap">
    <div class="error-code bg-primary flex items-center content-center justify-center">
      Login
    </div>
    <div>
      <div class="error-card shadow-4 bg-white column items-center justify-center no-wrap">
        <q-tabs align="justify" v-if="numTabsVisible > 0" v-model="selectedTab">
          <q-tab name="usernamePass" slot="title" label="Basic Auth" v-if="tabs.usernamePass"/>
          <q-tab name="xxx" slot="title" label="XXX" v-if="tabs.xxx"/>

          <q-tab-pane name="usernamePass">
            <q-input v-model="usernamePass.username" placeholder="Username" />
            <br>
            <q-input type="password" v-model="usernamePass.password" placeholder="Password" />
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
      Version: {{connectionData.version}}
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
  QInput,
  Loading,
  Notify
} from 'quasar'
import globalStore from '../store/globalStore'
import basicauthlogintogetjwttokenstore from '../store/basicauthlogintogetjwttoken'

export default {
  components: {
    QBtn,
    QIcon,
    QTabs,
    QTab,
    QTabPane,
    QInput
  },
  data () {
    return {
      tabs: {
        // JSON tag names must match tab name
        usernamePass: false,
        xxx: false
      },
      selectedTab: undefined,
      usernamePass: {
        username: '',
        password: ''
      },
      authmethod: undefined
    }
  },
  computed: {
    connectionData () {
      return globalStore.getters.connectionData
    },
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
      globalStore.commit('SET_APIFN', TTT.$callDockjobAPI)
      if (globalStore.getters.datastoreState === 'INITIAL') {
        Loading.show()
        var callback = {
          ok: function (response) {
            Loading.hide()
            if (globalStore.getters.datastoreState === 'INITIAL') {
              console.log('Error state STILL initial - stopping infinite loop')
            } else {
              // TTT.$router.replace(TTT.$route.query.redirect || '/')
              TTT.creationHandler()
            }
          },
          error: function (response) {
            Loading.hide()
            console.log('Error frontend connection data state: ' + response.message)
            Notify.create(response.message)
          }
        }
        globalStore.dispatch('init', {callback: callback})
        return
      }
      if (globalStore.getters.datastoreState === 'REQUIRE_LOGIN') {
        this.tabs.usernamePass = false
        this.tabs.xxx = false
        for (var i = 0; i < globalStore.getters.connectionData.apiaccesssecurity.length; i++) {
          var curAuthMethod = globalStore.getters.connectionData.apiaccesssecurity[i]
          this.authmethod = curAuthMethod
          if (curAuthMethod.type === 'basic-auth') this.tabs.usernamePass = true
          if (curAuthMethod.type === 'basic-auth-login-toget-jwttoken') this.tabs.usernamePass = true
        }
        for (var tab in this.tabs) {
          if (this.tabs[tab]) {
            this.selectedTab = tab
          }
        }
        return
      }
      // If there is no auth the state jumps direct from INITIAL to LOGGED_IN and dosen't revisit router page
      if (globalStore.getters.datastoreState === 'LOGGED_IN') {
        TTT.$router.replace(TTT.$route.query.redirect || '/')
        return
      }
      Notify.create('Invalid state ' + globalStore.getters.datastoreState)
      console.log('TODO deal with state ' + globalStore.getters.datastoreState)
    },
    usernamePassLogin () {
      var TTT = this
      var callback = {
        ok: function (response) {
          TTT.$router.replace(TTT.$route.query.redirect || '/')
        },
        error: function (response) {
          Notify.create(response.message)
        }
      }
      var accessCredentials = {
        type: 'basic-auth',
        username: this.usernamePass.username,
        password: this.usernamePass.password
      }
      if (this.authmethod.type === 'basic-auth-login-toget-jwttoken') {
        // Redirect API function to allow jwt token store to check for token expiry
        globalStore.commit('SET_APIFN',
          function callDockjobAPI (apiurl, dockJobAccessCredentials, method, pathWithoutStartingSlash, postdata, callback) {
            basicauthlogintogetjwttokenstore.dispatch('callAPI', {
              apifn: TTT.$callDockjobAPI,
              apiurl: apiurl,
              dockJobAccessCredentials: dockJobAccessCredentials,
              method: method,
              pathWithoutStartingSlash: pathWithoutStartingSlash,
              postdata: postdata,
              callback: callback
            })
          }
        )
        // Vue Store will call the login service and set cookie
        var callback2 = {
          ok: function (response) {
            globalStore.dispatch('login', {callback: callback, accessCredentials: undefined})
          },
          error: function (response) {
            callback.error(response)
          }
        }
        basicauthlogintogetjwttokenstore.dispatch('login', {callback: callback2, username: this.usernamePass.username, password: this.usernamePass.password, authmethod: this.authmethod})
      } else {
        globalStore.dispatch('login', {callback: callback, accessCredentials: accessCredentials})
      }
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
