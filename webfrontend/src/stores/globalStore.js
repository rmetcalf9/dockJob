// Global Store - contains server information, and user information
import Vue from 'vue'
import Vuex from 'vuex'

const state = {
  pageTitle: 'Default Page Title'
}

const mutations = {
  SET_PAGE_TITLE (state, link) {
    state.pageTitle = 'DockJob by RJM - ' + link
  }
}

const getters = {
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
