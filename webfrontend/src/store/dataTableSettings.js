// Global Store - contains server information, and user information
import Vue from 'vue'
import Vuex from 'vuex'

const state = {
  jobs: {
    visibleColumns: ['name', 'enabled', 'lastRunReturnCode', 'nextScheduledRun'],
    serverPagination: {
      page: 1,
      rowsNumber: 10, // specifying this determines pagination is server-side
      rowsPerPage: 10,
      sortBy: null,
      descending: false
    },
    filter: ''
  },
  jobExecutions: {
    visibleColumns: ['executionName', 'stage', 'resultReturnCode'],
    serverPagination: {
      page: 1,
      rowsNumber: 10, // specifying this determines pagination is server-side
      rowsPerPage: 10,
      sortBy: null,
      descending: false
    },
    filter: ''
  }
}

export const mutations = {
  JOBS (state, jobs) {
    state.jobs = jobs
  },
  JOBEXECUTIONS (state, jobExecutions) {
    state.jobExecutions = jobExecutions
  }
}

export const actions = {
}

const getters = {
  Jobs: (state, getters) => {
    return state.jobs
  },
  jobExecutions: (state, getters) => {
    return state.jobExecutions
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
