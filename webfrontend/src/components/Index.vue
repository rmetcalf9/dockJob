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
        <span slot="subtitle">Scheduled Job Runner</span>
      </q-toolbar-title>

    </q-toolbar>

    <q-scroll-area slot="left" style="width: 100%; height: 100%">
      <q-list-header>Navigation</q-list-header>

      <q-side-link item to="/dashboard">
        <q-item-side icon="home" />
        <q-item-main label="Dashboard" />
      </q-side-link>

    </q-scroll-area>

    <router-view />

    <q-toolbar slot="footer">
        <a href="https://github.com/rmetcalf9/dockJob">GitHub</a>
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
  QScrollArea
} from 'quasar'
import globalStore from './globalStore'

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
      return globalStore.state.pageTitle
    }
  },
  methods: {
  }
}
</script>
