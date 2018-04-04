// Global Store - contains server information, and user information
import Vue from 'vue'
import Vuex from 'vuex'
import { date } from 'quasar'

const state = {
  usersTimezone: 'UNSET',
  timestampFormat: 'DD-MMM-YY HH:mm:ss'
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
    // uses quasar dateutils http://quasar-framework.org/components/date-utils.html
    return function (iso8601String) {
      if (typeof (iso8601String) === 'undefined') {
        return undefined
      }
      if (iso8601String === null) {
        return null
      }
      var d = Date.parse(iso8601String)
      return date.formatDate(d, state.timestampFormat)
      // During testing this displayed in my local timezone
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
