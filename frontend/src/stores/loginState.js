import { defineStore } from 'pinia'

export const useLoginStateStore = defineStore('loginStateStore', {
  state: () => ({
    loggedinData: false,
    loginCredentials: {}
  }),

  getters: {
    loggedin (state) {
      return state.loggedinData
    }
  },

  actions: {
    setLoggedin (loginCredentials) {
      this.loggedinData = true
      this.loginCredentials = loginCredentials
    },
    setLoggedout () {
      this.loggedinData = false
    }
  }
})
