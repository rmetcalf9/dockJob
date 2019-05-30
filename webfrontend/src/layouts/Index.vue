<template>
  <q-layout
  >
    <q-header>
      <!-- First row of header is a QToolbar -->
      <q-toolbar>
        <!-- showLeft is a model attached to left side drawer below -->
        <q-btn
          flat round dense
          @click="showLeft = !showLeft"
          icon="menu"
        />
        <q-btn v-if="backroute !== ''" class="within-iframe-hide" flat @click="$router.replace(backroute)" style="margin-right: 15px">
          <q-icon name="keyboard_arrow_left" />
        </q-btn>

        <q-toolbar-title>
          {{ pageTitle }}
          <span slot="subtitle">dockJob - Scheduled Job Runner by RJM</span>
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <!-- Left Side Drawer -->
    <q-drawer side="left" v-model="showLeft">
      <q-list no-border link inset-separator>
        <q-item-label header>Navigation</q-item-label>
        <q-item to="/dashboard">
          <q-item-section avatar>
            <q-icon color="primary" name="home" />
          </q-item-section>
          <q-item-section>Dashboard</q-item-section>
        </q-item>
        <q-item to="/jobs">
          <q-item-section avatar>
            <q-icon color="primary" name="rowing" />
          </q-item-section>
          <q-item-section>Jobs</q-item-section>
        </q-item>
        <q-item to="/executions">
          <q-item-section avatar>
            <q-icon color="primary" name="play_arrow" />
          </q-item-section>
          <q-item-section>Executions</q-item-section>
        </q-item>
        <q-separator  v-if="loginRequiredByServer" />
        <q-item to="/logout"  v-if="loginRequiredByServer">
          <q-item-section avatar>
            <q-icon color="primary" name="exit_to_app" />
          </q-item-section>
          <q-item-section>Logout</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer>
      <q-toolbar>
        <table width="100%"><tr>
        <td>
          <a v-if="! (connectionData.apidocsurl === '_')" v-bind:href="connectionData.apidocsurl" target="_blank">APIdocs</a>
          <a href="https://github.com/rmetcalf9/dockJob" target="_blank">GitHub</a>
        </td>
        <td align="right">Version: {{connectionData.version}}</td>
        </tr></table>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script>
import {
  QLayout,
  QToolbar,
  QToolbarTitle,
  QTabs,
  QRouteTab,
  QBtn,
  QIcon,
  QItemSection,
  QItemLabel,
  QScrollArea,
  Loading,
  Notify
} from 'quasar'
import globalStore from '../store/globalStore'

export default {
  components: {
    QLayout,
    QToolbar,
    QToolbarTitle,
    QTabs,
    QRouteTab,
    QBtn,
    QIcon,
    QItemSection,
    QItemLabel,
    QScrollArea
  },
  data () {
    return {
      showLeft: true
    }
  },
  computed: {
    backroute () {
      // console.log(this.$route.path)
      if (this.$route.path === '/') return ''
      var x = this.$route.path.split('/')
      var o = ''
      for (var y in x) {
        if (y < (x.length - 1)) o += '/' + x[y]
      }
      var newPath = o.substring(1)
      return newPath
    },
    pageTitle () {
      return globalStore.getters.pageTitle
    },
    connectionData () {
      return globalStore.getters.connectionData
    },
    loginRequiredByServer () {
      return globalStore.getters.loginRequiredByServer
    }
  },
  methods: {
  },
  created () {
    if (globalStore.getters.datastoreState !== 'LOGGED_IN_SERVERDATA_LOADED') {
      Loading.show()
      var callback = {
        ok: function (response) {
          Loading.hide()
        },
        error: function (response) {
          Loading.hide()
          Notify.create(response.message)
        }
      }
      globalStore.dispatch('getServerInfo', {callback: callback})
    }
  }
}
</script>
