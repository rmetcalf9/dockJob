// function to wrap calls to dockjob API.
// this function is used normally, for testing it is substituted with a different function
import axios from 'axios'
import callbackHelper from 'callbackHelper'

function addAccessCredentials (config, dockJobAccessCredentials) {
  if (typeof (dockJobAccessCredentials) === 'undefined') {
    return config
  }
  if (dockJobAccessCredentials.type === 'basic-auth') {
    config.headers.Authorization = 'Basic ' + btoa(dockJobAccessCredentials.username + ':' + dockJobAccessCredentials.password)
    return config
  }
  return config
}

export default function callDockjobAPI (apiurl, dockJobAccessCredentials, method, pathWithoutStartingSlash, postdata, callback) {
  var config = {
    method: method,
    url: apiurl + '/' + pathWithoutStartingSlash,
    data: postdata
  }
  config = addAccessCredentials(config, dockJobAccessCredentials)
  // console.log(config)
  axios(config).then(
    (response) => {
      callback.ok(response)
    },
    (response) => {
      var rjmmsg = 'Error'

      if (typeof (response.response) === 'undefined') {
        if (typeof (response.message) === 'undefined') {
          rjmmsg = 'Bad Response UNKNOWN'
        }
        else {
          rjmmsg = 'Bad Response ' + response.message
        }
      }
      else if (typeof (response.response.data) !== 'undefined') {
        if (typeof (response.response.data.errorMessages) !== 'undefined') {
          rjmmsg = 'Bad Response(' + response.response.data.errorMessages.length + ') ' + response.response.data.errorMessages
        }
        else {
          rjmmsg = 'Data Bad Response ' + response.response.status
        }
      }
      else {
        rjmmsg = 'Nested Bad Response ' + response.response.status
      }
      callbackHelper.callbackHelper(callback, rjmmsg, response)
    }
  )
}
