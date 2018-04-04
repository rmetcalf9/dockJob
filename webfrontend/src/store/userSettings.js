// Global Store - contains server information, and user information
import Vue from 'vue'
import Vuex from 'vuex'

const state = {
  usersTimezone: 'UNSET',
  timestampFormat: 'XXX'
}

export const mutations = {
  // SET_PAGE_TITLE (state, link) {
  //  state.pageTitle = link
  // },
}

export const actions = {
}

const getters = {
  userTimeStringFN: (state, getters) => {
    return function (iso8601String) {
      if (typeof (iso8601String) === 'undefined') {
        return undefined
      }
      if (iso8601String === null) {
        return null
      }
      return 'TODO' + state.usersTimezone + ':' + state.timestampFormat + ':' + iso8601String
    }
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
