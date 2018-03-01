// import something here (http://quasar-framework.org/guide/app-plugins.html)
// function to wrap calls to dockjob API.
// this function is used normally, for testing it is substituted with a different function
import axios from 'axios'
import callbackHelper from '../callbackHelper'

// I don't think I can call globalstore from a plugin
// import globalStore from '../stores/globalStore'

function addAccessCredentials (config, dockJobAccessCredentials) {
  if (typeof (dockJobAccessCredentials) === 'undefined') {
    return config
  }
  if (dockJobAccessCredentials.type === 'basic-auth') {
    // config.headers.Authorization = 'Basic ' + btoa(dockJobAccessCredentials.username + ':' + dockJobAccessCredentials.password)
    config.auth = {
      username: dockJobAccessCredentials.username,
      password: dockJobAccessCredentials.password
    }
    return config
  }
  return config
}

function callDockjobAPI (apiurl, dockJobAccessCredentials, method, pathWithoutStartingSlash, postdata, callback) {
  var config = {
    method: method,
    url: apiurl + '/' + pathWithoutStartingSlash,
    data: postdata
  }
  config = addAccessCredentials(config, dockJobAccessCredentials)
  axios(config).then(
    (response) => {
      callback.ok(response)
    },
    (response) => {
      callbackHelper.webserviceError(callback, response)
    }
  )
}

// leave the export, even if you don't use it
export default ({ app, router, Vue }) => {
  Vue.prototype.$callDockjobAPI = callDockjobAPI
  // globalStore.commit('SET_APIFN', callDockjobAPI)
}
