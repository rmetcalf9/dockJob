import { defineStore } from 'pinia'

export const useLoginStateStore = defineStore('loginStateStore', {
  state: () => ({
    loggedinData: false
  }),

  getters: {
    loggedin (state) {
      return state.loggedinData
    }
  },

  actions: {
    increment () {
      this.counter++
    }
  }
})
