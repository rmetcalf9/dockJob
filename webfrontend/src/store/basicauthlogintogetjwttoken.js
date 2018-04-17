// store for auth information
import Vue from 'vue'
import Vuex from 'vuex'

import axios from 'axios'
import callbackHelper from '../callbackHelper'

const state = {
  username: undefined,
  password: undefined,
  authmethod: undefined,
  token: undefined
}

export const mutations = {
  SET_USERNAMEANDPASSWORDANDAUTHMETHOD (state, values) {
    state.username = values.username
    state.password = values.password
    state.authmethod = values.authmethod
    state.token = undefined
  },
  SET_TOKEN (state, value) {
    state.token = value
  }
}

export const actions = {
  login ({commit, state, dispatch}, params) {
    // Expecting
    //  params.callback
    //  params.username
    //  params.password
    //  params.authmethod.type = basic-auth-login-toget-jwttoken
    //  params.authmethod.loginurl
    //  params.authmethod.cookiename = basic-auth-login-toget-jwttoken
    commit('SET_USERNAMEANDPASSWORDANDAUTHMETHOD', {username: params.username, password: params.password, authmethod: params.authmethod})
    dispatch('getJWT', params)
  },
  getJWT ({commit, state, dispatch}, params) {
    var config = {
      method: 'get',
      url: state.authmethod.loginurl,
      auth: {
        username: state.username,
        password: state.password
      }
    }
    axios(config).then(
      (response) => {
        commit('SET_TOKEN', response.data)
        // TODO Consider adding an expiry to this cookie
        var cookie = escape(state.authmethod.cookiename) + '=' + escape(state.token.JWTToken) + ';'
        document.cookie = cookie
        params.callback.ok(response)
      },
      (response) => {
        callbackHelper.webserviceError(params.callback, response)
      }
    )
  },
  callAPI ({commit, state, dispatch}, params) {
    console.log('TODO Implement API 222')
    params.apifn(params.apiurl, params.dockJobAccessCredentials, params.method, params.pathWithoutStartingSlash, params.postdata, params.callback)
  }
}

const getters = {
}

Vue.use(Vuex)

// Vuex version
export default new Vuex.Store({
  state,
  mutations,
  getters,
  actions
})
