// Global Store - contains server information, and user information
import Vue from 'vue'
import Vuex from 'vuex'

// using a function to return different instances
function defaultTableSettings () {
  return {
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
  jobExecutions: defaultTableSettings(),
  prefixedDataTableSettings: {}
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
  },
  prefixedDataTableSetting: (state, getters) => {
    // This stops cacheing taking place
    return function (key) {
      if (typeof (state.prefixedDataTableSettings[key]) === 'undefined') {
        state.prefixedDataTableSettings[key] = defaultTableSettings()
      }
      return state.prefixedDataTableSettings[key]
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
