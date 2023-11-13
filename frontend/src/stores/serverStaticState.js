import { defineStore } from 'pinia'
import axios from 'axios'

function tryToGetServerData({locationsToTry, successCallback}) {
  if (locationsToTry.length === 0) {
    console.log('ERROR Failed to get server static data')
    return
  }
  const toTry = locationsToTry.pop()

  console.log('Trying to get server info from:', toTry)

  var config = {
    method: 'GET',
    url: toTry
  }
  axios(config).then(
    (response) => {
      successCallback(response)
    },
    (response) => {
      tryToGetServerData({
        locationsToTry: locationsToTry,
        successCallback: successCallback
      })
    }
  )
}

export const useServerStaticStateStore = defineStore('useServerStaticStateStore', {
  state: () => ({
    loaded: false,
    serverInfoData: { 'x': 'y' }
  }),

  getters: {
    serverInfo (state) {
      return state.serverInfoData
    }
  },

  actions: {
    loadState () {
      let TTT = this
      this.loaded = true

      const hostname = window.location.host.split(":")[0]

      //We could be
      // in prod (Behing Kong AND nginx)
      // in docker port 8310 behind nginx
      // nativly on local machine

      const locationsToTry = [
        'webfrontendConnectionData',
        '/webfrontendConnectionData',
        'http://' + hostname + ':8301/webfrontendConnectionData',
        'http://' + hostname + ':8098/frontend/webfrontendConnectionData',
      ]
      tryToGetServerData({
        locationsToTry: locationsToTry.reverse(),
        successCallback: TTT._loadState
      })
    },
    _loadState (newState) {
      this.serverInfoData = newState
    }
  }
})
