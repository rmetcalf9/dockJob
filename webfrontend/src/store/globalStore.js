// Global Store - contains server information, and user information
import Vue from 'vue'
import Vuex from 'vuex'
// import callbackHelper from 'callbackHelper'
import webfrontendConnectionData from '../webfrontendConnectionData'

// Exports MUST be in sequence

export const getInitialState = function () {
  return {
    datastoreState: 'INITIAL', // INITIAL, REQUIRE_LOGIN, LOGGED_IN, LOGGED_IN_SERVERDATA_LOADED
    loginRequiredByServer: false,
    APIFn: undefined,
    accessCredentials: undefined,
    pageTitle: 'Default Page Title',
    connectionData: { version: 'UNKNOWN' }, // Data retrieved from this server (no security)
    serverInfo: undefined // Data retrieved from server info service call
  }
}

export const mutations = {
  SET_PAGE_TITLE (state, link) {
    state.pageTitle = link
  },
  SET_APIFN (state, apifn) {
    state.APIFn = function (method, pathWithoutStartingSlash, postdata, callbackfn) {
      return apifn(state.connectionData.apiurl, state.accessCredentials, method, pathWithoutStartingSlash, postdata, callbackfn)
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
      state.loginRequiredByServer = false
    } else {
      state.datastoreState = 'REQUIRE_LOGIN'
      state.loginRequiredByServer = true
    }
  },
  // Only to be called from this file, use actions
  SET_ACCESSCREDENTIALS (state, accessCredentials) {
    state.accessCredentials = accessCredentials
  },
  // Only to be called from this file, use actions
  SET_STORESTATE (state, value) {
    state.datastoreState = value
  }
}

export const actions = {
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
    state.APIFn('GET', 'serverinfo/', undefined, callback)
  },
  login ({commit, state}, params) {
    commit('SET_ACCESSCREDENTIALS', params.accessCredentials)
    var callback = {
      ok: function (response) {
        commit('SET_SERVERINFO', response.data)
        params.callback.ok(response)
      },
      error: function (error) {
        params.callback.error(error)
      }
    }
    state.APIFn('GET', 'serverinfo/', undefined, callback)
  },
  logout ({commit, state}, params) {
    commit('SET_ACCESSCREDENTIALS', undefined)
    commit('SET_STORESTATE', 'REQUIRE_LOGIN')
    params.callback.ok(undefined)
  }
}

const state = getInitialState()

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
  },
  loginRequiredByServer: (state, getters) => {
    return state.loginRequiredByServer
  },
  apiFN: (state, getters) => {
    return state.APIFn
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
