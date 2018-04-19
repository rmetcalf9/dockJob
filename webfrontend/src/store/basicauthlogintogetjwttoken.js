// store for auth information
import Vue from 'vue'
import Vuex from 'vuex'

import axios from 'axios'
import callbackHelper from '../callbackHelper'
import { Cookies } from 'quasar'

const state = {
  username: undefined,
  password: undefined,
  authmethod: undefined,
  token: undefined
}

var isCookieSetFN = function () {
  var r = Cookies.has(state.authmethod.cookiename)
  if (r === false) {
    return false
  }
  return Cookies.get(state.authmethod.cookiename) !== ''
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
  logout ({commit, state, dispatch}, params) {
    if (isCookieSetFN()) {
      // Note- remove cookie not working so we settle for blanking out the value and setting it to expire
      Cookies.set(state.authmethod.cookiename, 'X', {secure: true, path: '/', expire: -1})
      Cookies.set(state.authmethod.cookiename, '', {secure: true, path: '/', expire: -1})
      Cookies.remove(state.authmethod.cookiename)
    }
    commit('SET_TOKEN', undefined)
    params.callback.ok(undefined)
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
        // Not adding expire to the cookie as we are making it a session cookie
        //  expire can ounly be quoted in days
        Cookies.set(state.authmethod.cookiename, state.token.JWTToken, {secure: true, path: '/'})
        params.callback.ok(response)
      },
      (response) => {
        callbackHelper.webserviceError(params.callback, response)
      }
    )
  },
  callAPI ({commit, state, dispatch}, params) {
    if (!Cookies.has(state.authmethod.cookiename)) {
      console.log('ERROR in basicauthlogintogetjwttoken.js -> callAPI')
      console.log('No cookie present - user needs to log in should never get here')
      callbackHelper.callbackWithSimpleError(params.callback, 'No security cookie present')
    } else {
      var callback2 = {
        ok: params.callback.ok,
        error: function (response) {
          if (typeof (response.orig) !== 'undefined') {
            if (typeof (response.orig.response) !== 'undefined') {
              if (typeof (response.orig.response.status) !== 'undefined') {
                if (response.orig.response.status === 401) {
                  console.log('Got 401 on first service call - trying to get a new token')
                  var paramsToSendTogetJWT = {
                    callback: {
                      ok: function (response) {
                        // Second call callback function is the origional callback function because that will have no retry
                        params.apifn(params.apiurl, params.dockJobAccessCredentials, params.method, params.pathWithoutStartingSlash, params.postdata, params.callback)
                      },
                      error: params.callback.error
                    }
                  }
                  dispatch('getJWT', paramsToSendTogetJWT)
                  return
                }
              }
            }
          }
          params.callback.error(response)
        }
      }
      params.apifn(params.apiurl, params.dockJobAccessCredentials, params.method, params.pathWithoutStartingSlash, params.postdata, callback2)
    }
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
