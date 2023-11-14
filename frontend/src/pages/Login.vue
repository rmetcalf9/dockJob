<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page padding>
        <div>
          <div class="fullscreen bg-blue text-white text-center q-pa-md flex flex-center">
              <div class="row">
                <div class="col">
                  <div class="text-h2" style="opacity:.4">
                    Login
                  </div>
                  <q-card padding>
                    <div class="q-pa-md">
                      <q-input v-model="usernamePass.username" placeholder="Username" />
                      <br>
                      <q-input type="password" v-model="usernamePass.password" placeholder="Password" />
                      <br>
                      <p class="text-center group">
                        <q-btn
                          color="primary"
                          push
                          @click="usernamePassLogin"
                        >
                          Login to dockjob
                        </q-btn>
                      </p>
                    </div>
                  </q-card>
                  <div>
                    Version: {{serverInfo.data.version}}
                  </div>
                </div>
              </div>
          </div>
        </div>
      </q-page>
    </q-page-container>

  </q-layout>
</template>

<script>
// I am only implementing basic auth here and ignoring the JWT method
//  if login fails I will rely on a 403 sending the user back here
import { useServerStaticStateStore } from 'stores/serverStaticState'
import { useLoginStateStore } from 'stores/loginState'
import { Notify } from 'quasar'

export default {
  name: 'App-Login',
  setup () {
    const serverStaticState = useServerStaticStateStore()
    const loginStateStore = useLoginStateStore()
    return { serverStaticState, loginStateStore }
  },
  data () {
    return {
      selectedTab: undefined,
      usernamePass: {
        username: '',
        password: ''
      }
    }
  },
  computed: {
    serverInfo () {
      const serverInfo = this.serverStaticState.serverInfo
      if ( this.serverStaticState.isLoaded) {
        if (!this.serverStaticState.loginRequired) {
          console.log('No Security for login')
          this.loginStateStore.setLoggedin({})
          this.$router.replace('/')
        }
      }
      return serverInfo
    },
  },
  methods: {
    usernamePassLogin () {
      this.loginStateStore.setLoggedin(this.usernamePass)
      this.$router.replace('/')
      // Notify.create({
      //  color: 'negative',
      //  message: 'Not Implmemented'
      // })
      // console.log('TODO')
    }
  },
  mounted () {
    this.serverStaticState.loadState()
  }
}
</script>
