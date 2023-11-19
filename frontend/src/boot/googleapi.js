import { boot } from 'quasar/wrappers'

export default boot(({ app }) => {
  window.gapi.load('client')
  app.config.globalProperties.$gapi = window.gapi
})
