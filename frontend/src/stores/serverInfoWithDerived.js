import { defineStore } from 'pinia'

export const useServerInfoWithDerivedStore = defineStore('serverInfoWithDerivedStore', {
  state: () => ({
    loaded: false,
    serverInfoWithDerivedData: {
    }
  }),

  getters: {
    isLoaded (state) {
      return state.loaded
    },
    serverInfoWithDerived (state) {
      return state.serverInfoWithDerivedData
    }
  },

  actions: {
    refresh ({force, callback, wrappedCallApiFn}) {
      const TTT = this
      if (this.laoded) {
        if (!force) {
          return
        }
      }
      var callbackInternal = {
        ok: function (response) {
          TTT.saveServerInfoWithDerived({serverInfo: response.data})
          callback.ok(response)
        },
        error: function (error) {
          callback.error(error)
        }
      }
      // Need slash because without slash is different endpoint
      wrappedCallApiFn({
        method: 'get',
        path: '/serverinfo', // without trailing slash different DATA!!
        postdata: undefined,
        callback: callbackInternal
      })
    },
    saveServerInfoWithDerived ({serverInfo}) {
      this.serverInfoWithDerivedData = serverInfo
      this.loaded = true
    }
  }
})
