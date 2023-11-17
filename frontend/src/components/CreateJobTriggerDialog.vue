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
            <div v-if="selectedType === ''">
              <div class="column wrap justify-center items-center content-center q-gutter-lg">
                <div>Select type of trigger</div>
                <div v-for="type in Object.keys(serverInfoWithDerived.Derived.ExternalTriggers.types)" v-bind:key="type">
                  <q-btn
                    color="primary"
                    :label="type"
                    @click="selectTriggerType(type)"
                  />
                </div>
              </div>
            </div>
            <div v-if="selectedType === 'googleDriveRawClass'">
              <ExternalTriggerGoogleDriveRawClass
                :jobData="jobData"
                @triggercreated="triggercreated"
              />
            </div>
            <div v-if="selectedType === 'googleDriveNewFileWatchClass'">
              <ExternalTriggerGoogleDriveNewFileWatchClass
                :jobData="jobData"
                @triggercreated="triggercreated"
              />
            </div>
          </q-page>
        </q-page-container>

        <q-footer class="bg-black text-white">
          <q-toolbar inset>
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

import ExternalTriggerGoogleDriveRawClass from '../components/externalTrigger/googleDriveRawClass/create.vue'
import ExternalTriggerGoogleDriveNewFileWatchClass from '../components/externalTrigger/googleDriveNewFileWatchClass/create.vue'



export default {
  name: 'Modal-CreateJob',
  props: [
    'jobData'
  ],
  components: {
    ExternalTriggerGoogleDriveRawClass,
    ExternalTriggerGoogleDriveNewFileWatchClass
  },
  setup () {
    const serverInfoWithDerivedStore = useServerInfoWithDerivedStore()
    const loginStateStore = useLoginStateStore()
    const serverStaticStateStore = useServerStaticStateStore()

    return { loginStateStore, serverStaticStateStore, serverInfoWithDerivedStore }
  },
  data () {
    return {
      dialogVisible: false,
      selectedType: ''
    }
  },
  methods: {
    triggercreated () {
      this.$emit('triggercreated')
      this.dialogVisible = false
    },
    selectTriggerType (type) {
      this.selectedType = type
    },
    openCreateJobTriggerDialog () {
      this.selectedType = ''
      this.dialogVisible = true
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
