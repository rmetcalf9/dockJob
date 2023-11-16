<template>
    <q-dialog v-model="dialogVisible">
      <q-layout view="Lhh lpR fff" container class="bg-white" style="width: 700px; max-width: 80vw;">
        <q-header class="bg-primary">
          <q-toolbar>
            <q-toolbar-title>
              Add external trigger
            </q-toolbar-title>
            <q-btn flat v-close-popup round dense icon="close" />
          </q-toolbar>
        </q-header>

        <q-page-container>
          <q-page padding>
            {{ serverInfoWithDerived }}
          </q-page>
        </q-page-container>

        <q-footer class="bg-black text-white">
          <q-toolbar inset>
            <q-btn
              color="primary"
              label="ok"
              @click="createTriggerMethod"
            />
            <q-btn
              v-close-popup
              label="Cancel"
            />
          </q-toolbar>
        </q-footer>
      </q-layout>
    </q-dialog>
</template>

<script>
import callDockjobBackendApi from '../callDockjobBackendApi'

import { useServerInfoWithDerivedStore } from 'stores/serverInfoWithDerived'
import { useLoginStateStore } from 'stores/loginState'
import { useServerStaticStateStore } from 'stores/serverStaticState'


export default {
  name: 'Modal-CreateJob',
  components: {
  },
  setup () {
    const serverInfoWithDerivedStore = useServerInfoWithDerivedStore()
    const loginStateStore = useLoginStateStore()
    const serverStaticStateStore = useServerStaticStateStore()

    return { loginStateStore, serverStaticStateStore, serverInfoWithDerivedStore }
  },
  data () {
    return {
      dialogVisible: false
    }
  },
  methods: {
    openCreateJobTriggerDialog () {
      this.dialogVisible = true
    },
    createTriggerMethod () {
      this.dialogVisible = false
    }
  },
  computed: {
    serverInfoWithDerived () {
      return this.serverInfoWithDerivedStore.serverInfoWithDerived
    }
  },
  mounted () {
    const TTT = this
    const wrappedCallApiFn = callDockjobBackendApi.getWrappedCallApi({
      loginStateStore: TTT.loginStateStore,
      apiurl: TTT.serverStaticStateStore.staticServerInfo.data.apiurl
    })
    this.serverInfoWithDerivedStore.refresh({
      force: false,
      callback: undefined,
      wrappedCallApiFn
    })
  }
}

</script>
