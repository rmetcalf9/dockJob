import { defineStore } from 'pinia'

function defaultTableSettings () {
  return {
    visibleColumns: ['dateStarted', 'jobName', 'executionName', 'stage', 'resultReturnCode'],
    serverPagination: {
      page: 1,
      rowsNumber: 10, // specifying this determines pagination is server-side
      rowsPerPage: 10,
      sortBy: 'dateStarted',
      descending: true
    },
    filter: ''
  }
}

export const useDataTableSettingsStore = defineStore('dataTableSettingsStore', {
  state: () => ({
    allSettings: {}
  }),

  getters: {
    getSettings (state) {
      return function (name) {
        if (typeof (state.allSettings[name]) === 'undefined') {
          state.allSettings[name] = defaultTableSettings()
        }
        return state.allSettings[name]
      }
    }
  },

  actions: {
    increment () {
      this.counter++
    }
  }
})
