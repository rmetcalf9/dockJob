import { defineStore } from 'pinia'

export const useLoginStateStore = defineStore('loginStateStore', {
  state: () => ({
    loggedinData: false,
    loginCredentials: {},
    loginType: undefined
  }),

  getters: {
    loggedin (state) {
      return state.loggedinData
    }
  },

  actions: {
    setLoggedin ({loginCredentials, loginType}) {
      this.loggedinData = true
      this.loginCredentials = loginCredentials
      this.loginType = loginType
    },
    setLoggedout () {
      this.loggedinData = false
    }
  }
})
