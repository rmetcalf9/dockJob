<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          Dockjob
        </q-toolbar-title>

        <div>Quasar v{{ $q.version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label
          header
        >
          Navigation
        </q-item-label>
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
        <q-separator />
        <q-item to="/logout">
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
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useLoginStateStore } from 'stores/loginState'

export default defineComponent({
  name: 'MainLayout',

  components: {
  },

  setup () {
    const leftDrawerOpen = ref(false)
    const loginStateStore = useLoginStateStore()

    return {
      loginStateStore,
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  },
  computed: {
  },
  mounted () {
    if (!this.loginStateStore.loggedin) {
      this.$router.replace('/login')
    }
  }
})
</script>
