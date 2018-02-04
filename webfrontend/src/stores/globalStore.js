// Global Store - contains server information, and user information
import Vue from 'vue'
import Vuex from 'vuex'

import serverData from './serverData.js'

const state = {
  pageTitle: 'Default Page Title',
  serverData: serverData
}

const mutations = {
  SET_PAGE_TITLE (state, link) {
    state.pageTitle = 'DockJob by RJM - ' + link
  }
}

const getters = {
  pageTitle: (state, getters) => {
    return state.pageTitle
  },
  serverData: (state, getters) => {
    return state.serverData
  }
}

const actions = {
}

Vue.use(Vuex)

// Vuex version
export default new Vuex.Store({
  state,
  mutations,
  getters,
  actions
})
