// Functions to call the dockjob backend API
// if we get a 401 then set loginstate to not logged in to make system relogin
import axios from 'axios'


function addAccessCredentials (config, loginStateStore) {
  if (!loginStateStore.loggedin) {
    // not logged in
    return config
  }
  if (loginStateStore.loginType === 'basic-auth') {
    // config.headers.Authorization = 'Basic ' + btoa(dockJobAccessCredentials.username + ':' + dockJobAccessCredentials.password)
    config.auth = {
      username: loginStateStore.loginCredential.username,
      password: loginStateStore.loginCredential.password
    }
    return config
  }
  return config
}


function callApi({method, path, postdata, callback, loginStateStore, apiurl}) {
  var config = {
    method: method,
    url: apiurl + path,
    data: postdata
  }
  config = addAccessCredentials(config, loginStateStore)
  axios(config).then(
    (response) => {
      callback.ok(response)
    },
    (response) => {
      if (response.response.status === 401) {
        // User needs to login again
        loginStateStore.setLoggedout()
      }
      callback.error(response)
    }
  )
}

function getWrappedCallApi({loginStateStore, apiurl}) {
  return function ({method, path, postdata, callback}) {
    return callApi({method, path, postdata, callback, loginStateStore, apiurl})
  }
}


export default {
  callApi,
  getWrappedCallApi
}
