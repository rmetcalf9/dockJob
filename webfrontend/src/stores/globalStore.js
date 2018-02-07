// Global Store - contains server information, and user information
import Vue from 'vue'
import Vuex from 'vuex'

import serverData from './serverData.js'

const state = {
  dockJobAPIFn: undefined,
  dockJobAccessCredentials: undefined,
  pageTitle: 'Default Page Title',
  serverData: serverData, // Data retrieved from imported file
  serverInfo: undefined // Data retrieved from server info service call
}

const mutations = {
  SET_PAGE_TITLE (state, link) {
    state.pageTitle = link
  },
  SET_DOCKJOBAPIFN (state, dockjobapifn) {
    state.dockJobAPIFn = function (method, pathWithoutStartingSlash, postdata, callbackfn) {
      return dockjobapifn(state.serverData.apiurl, state.dockJobAccessCredentials, method, pathWithoutStartingSlash, postdata, callbackfn)
    }
  },
  SET_SERVERINFO (state, serverinfo) {
    state.serverInfo = serverinfo
  }
}

const getters = {
  pageTitle: (state, getters) => {
    return state.pageTitle
  },
  serverData: (state, getters) => {
    return state.serverData
  },
  serverInfo: (state, getters) => {
    return state.serverInfo
  }
}

const actions = {
  getServerInfo ({commit, state}, params) {
    var callback = {
      ok: function (response) {
        commit('SET_SERVERINFO', response.data)
        params.callback.ok(response)
      },
      error: function (error) {
        params.callback.error(error)
      }
    }
    state.dockJobAPIFn('GET', 'serverinfo', undefined, callback)
  }
}

Vue.use(Vuex)

// Vuex version
export default new Vuex.Store({
  state,
  mutations,
  getters,
  actions
})
