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
import { useServerStaticStateStore } from 'stores/serverStaticState'

export default {
  name: 'App-Login',
  setup () {
    const serverStaticState = useServerStaticStateStore()
    return { serverStaticState }
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
      return this.serverStaticState.serverInfo
    },
  },
  methods: {
    usernamePassLogin () {
      console.log('TODO')
    }
  },
  mounted () {
    this.serverStaticState.loadState()
  }
}
</script>
