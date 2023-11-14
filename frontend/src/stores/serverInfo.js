import { defineStore } from 'pinia'

export const useServerInfoStore = defineStore('serverInfoStore', {
  state: () => ({
    loaded: false,
    serverInfoData: { // Data retrieved from server info service call
      Server: {
        DefaultUserTimezone: 'Europe/London'
      }
    }
  }),

  getters: {
    isLoaded (state) {
      return state.loaded
    },
    serverInfo (state) {
      return state.serverInfoData
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
          TTT.saveServerInfo({serverInfo: response.data})
          callback.ok(response)
        },
        error: function (error) {
          callback.error(error)
        }
      }
      wrappedCallApiFn({
        method: 'get',
        path: '/serverinfo',
        postdata: undefined,
        callback: callbackInternal
      })
    },
    saveServerInfo ({serverInfo}) {
      this.serverInfoData = serverInfo
      this.loaded = true
    }
  }
})
