<template>
  <q-layout
    ref="layout"
    :view="layoutStore.view"
    :left-breakpoint="layoutStore.leftBreakpoint"
    :reveal="layoutStore.reveal"
  >
    <q-toolbar slot="header">
      <q-btn flat @click="$refs.layout.toggleLeft()">
        <q-icon name="menu" />
      </q-btn>
      <q-btn v-if="backroute !== ''" class="within-iframe-hide" flat @click="$router.replace(backroute)" style="margin-right: 15px">
        <q-icon name="keyboard_arrow_left" />
      </q-btn>
      <q-toolbar-title>
        {{ pageTitle }}
        <span slot="subtitle">dockJob - Scheduled Job Runner by RJM</span>
      </q-toolbar-title>
    </q-toolbar>

    <q-scroll-area slot="left" style="width: 100%; height: 100%">
      <q-list-header>Navigation</q-list-header>

      <q-side-link item to="/dashboard">
        <q-item-side icon="home" />
        <q-item-main label="Dashboard" />
      </q-side-link>
      <q-side-link item to="/dashboard2">
        <q-item-side icon="home" />
        <q-item-main label="Dashboard2" />
      </q-side-link>
      <hr v-if="loginRequiredByServer">
      <q-side-link item to="/logout" v-if="loginRequiredByServer">
        <q-item-side icon="exit_to_app" />
        <q-item-main label="Logout" />
      </q-side-link>

    </q-scroll-area>

    <router-view />
    <q-toolbar slot="footer">
        <table width="100%"><tr>
        <td>
          <a v-if="! (connectionData.apidocsurl === '_')" v-bind:href="connectionData.apidocsurl" target="_blank">APIdocs</a>
          <a href="https://github.com/rmetcalf9/dockJob" target="_blank">GitHub</a> 
        </td>
        <td align="right">Version: {{connectionData.version}}</td>
        </tr></table>
    </q-toolbar>
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
  QSideLink,
  QListHeader,
  QScrollArea,
  Loading,
  Toast
} from 'quasar'
import globalStore from '../stores/globalStore'

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
    QSideLink,
    QListHeader,
    QScrollArea
  },
  data () {
    return {
      layoutStore: {
      }
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
          Toast.create(response.message)
        }
      }
      globalStore.dispatch('getServerInfo', {callback: callback})
    }
  }
}
</script>
