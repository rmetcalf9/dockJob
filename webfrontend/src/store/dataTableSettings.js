// Global Store - contains server information, and user information
import Vue from 'vue'
import Vuex from 'vuex'

const state = {
  jobs: {
    visibleColumns: ['name', 'enabled', 'nextScheduledRun'],
    serverPagination: {
      page: 1,
      rowsNumber: 10, // specifying this determines pagination is server-side
      rowsPerPage: 10
    },
    filter: ''
  }
}

export const mutations = {
  JOBS (state, jobs) {
    state.jobs = jobs
  }
}

export const actions = {
}

const getters = {
  Jobs: (state, getters) => {
    return state.jobs
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
