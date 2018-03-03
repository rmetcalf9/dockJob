<template>
  <q-layout
  >
    <q-layout-header>
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
    </q-layout-header>

    <!-- Left Side Drawer -->
    <q-layout-drawer side="left" v-model="showLeft">
      <q-list no-border link inset-separator>
        <q-list-header>Navigation</q-list-header>
        <q-item to="/dashboard">
          <q-item-side icon="home" />
          <q-item-main label="Dashboard" sublabel="" />
        </q-item>
        <q-item to="/jobs">
          <q-item-side icon="rowing" />
          <q-item-main label="Jobs" sublabel="" />
        </q-item>
        <hr v-if="loginRequiredByServer">
        <q-item to="/logout" v-if="loginRequiredByServer">
          <q-item-side icon="exit_to_app" />
          <q-item-main label="Logout" Logout="" />
        </q-item>
      </q-list>
    </q-layout-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-layout-footer><q-toolbar>
        <table width="100%"><tr>
        <td>
          <a v-if="! (connectionData.apidocsurl === '_')" v-bind:href="connectionData.apidocsurl" target="_blank">APIdocs</a>
          <a href="https://github.com/rmetcalf9/dockJob" target="_blank">GitHub</a>
        </td>
        <td align="right">Version: {{connectionData.version}}</td>
        </tr></table>
    </q-toolbar></q-layout-footer>
  </q-layout>
</template>

<script>
import {
  QLayout,
  QToolbar,
  QToolbarTitle,
  QSearch,
  QTabs,
  QRouteTab,
  QBtn,
  QIcon,
  QItemSide,
  QItemMain,
  QListHeader,
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
    QSearch,
    QTabs,
    QRouteTab,
    QBtn,
    QIcon,
    QItemSide,
    QItemMain,
    QListHeader,
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
