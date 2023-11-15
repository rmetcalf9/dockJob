import { defineStore } from 'pinia'

function defaultTableSettings ({defaultVisibleColumns, defaultSortBy}) {
  return {
    visibleColumns: defaultVisibleColumns,
    serverPagination: {
      page: 1,
      rowsNumber: 10, // specifying this determines pagination is server-side
      rowsPerPage: 25,
      sortBy: defaultSortBy,
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
      return function ({name, defaultVisibleColumns, defaultSortBy}) {
        if (typeof (state.allSettings[name]) === 'undefined') {
          state.allSettings[name] = defaultTableSettings({defaultVisibleColumns, defaultSortBy})
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
