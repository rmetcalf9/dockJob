// Global Store - contains server information, and user information
import Vue from 'vue'
import Vuex from 'vuex'
// import callbackHelper from 'callbackHelper'
import webfrontendConnectionData from '../webfrontendConnectionData'

const state = {
  datastoreState: 'INITIAL', // INITIAL, REQUIRE_LOGIN, LOGGED_IN, LOGGED_IN_SERVERDATA_LOADED
  dockJobAPIFn: undefined,
  dockJobAccessCredentials: undefined,
  pageTitle: 'Default Page Title',
  connectionData: undefined, // Data retrieved from this server (no security)
  serverInfo: undefined // Data retrieved from server info service call
}

const mutations = {
  SET_PAGE_TITLE (state, link) {
    state.pageTitle = link
  },
  SET_DOCKJOBAPIFN (state, dockjobapifn) {
    state.dockJobAPIFn = function (method, pathWithoutStartingSlash, postdata, callbackfn) {
      return dockjobapifn(state.connectionData.apiurl, state.dockJobAccessCredentials, method, pathWithoutStartingSlash, postdata, callbackfn)
    }
  },
  SET_SERVERINFO (state, serverinfo) {
    state.datastoreState = 'LOGGED_IN_SERVERDATA_LOADED'
    state.serverInfo = serverinfo
  },
  SET_CONNECTIONDATA (state, connectionData) {
    state.connectionData = connectionData
    if (state.connectionData.apiaccesssecurity.length === 0) {
      state.datastoreState = 'LOGGED_IN' // no login required
    }
    else {
      state.datastoreState = 'REQUIRE_LOGIN'
    }
  }

}

const getters = {
  pageTitle: (state, getters) => {
    return state.pageTitle
  },
  connectionData: (state, getters) => {
    return state.connectionData
  },
  serverInfo: (state, getters) => {
    return state.serverInfo
  },
  datastoreState: (state, getters) => {
    return state.datastoreState
  }
}

const actions = {
  init ({commit, state}, params) {
    // init means we must load connection data
    var callback = {
      ok: function (response) {
        commit('SET_CONNECTIONDATA', response.data)
        params.callback.ok(response)
      },
      error: params.callback.error
    }
    webfrontendConnectionData(callback)
  },
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
