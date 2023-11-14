import { defineStore } from 'pinia'

export const useLoginStateStore = defineStore('loginStateStore', {
  state: () => ({
    loggedinData: false,
    loginCredentialData: {},
    loginTypeData: undefined
  }),

  getters: {
    loggedin (state) {
      return state.loggedinData
    },
    loginType (state) {
      return state.loginTypeData
    },
    loginCredential (state) {
      return state.loginCredentialData
    }
  },

  actions: {
    setLoggedin ({loginCredentials, loginType}) {
      this.loggedinData = true
      this.loginCredentialData = loginCredentials
      this.loginTypeData = loginType
    },
    setLoggedout () {
      this.loggedinData = false
      this.loginCredentialData = {}
    }
  }
})
