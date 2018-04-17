// Retrieve webfrontend connection data
//  If service call returns an error provide static development values
import axios from 'axios'
// import callbackHelper from 'callbackHelper'

// Try the first location in the list
function tryLocation (locationList, callback) {
  var toTry = locationList.pop()
  var config = {
    method: 'GET',
    url: toTry
  }
  axios(config).then(
    (response) => {
      callback.ok(response)
    },
    (response) => {
      if (locationList.length > 0) {
        tryLocation(locationList, callback)
      } else {
        var devBoxData = {
          version: 'Development-devBoxData', // Version show as 0 from this file
          apiurl: 'http://localhost:80/api',
          apiaccesssecurity: [] // all supported auth types. Can be empty, or JSON: basic-auth, jwt
          // Empty list means no auth type
          //  values documented here https://github.com/rmetcalf9/dockJob/blob/master/ENVVARIABLES.md
        }
        var basicAuthData = {
          version: 'Development-basicAuthData',
          apiurl: 'http://localhost:80/api',
          apiaccesssecurity: [{type: 'basic-auth'}]
        }
        var workLoginConnectionData = {
          version: 'Development-basicAuthData',
          apiurl: 'http://somefunnyhostname.com:5080/api',
          apidocsurl: 'http://somefunnyhostname.com:5080/apidocs',
          apiaccesssecurity: []
        }
        var a = false
        if (a) {
          console.log(devBoxData) // This is the one to use for localhost testing
          console.log(basicAuthData)
          console.log(workLoginConnectionData)
        }
        callback.ok({data: devBoxData})
      }
    }
  )
}

function getData (callback) {
  var locationsToTry = ['webfrontendConnectionData', '/webfrontendConnectionData', 'http://somefunnyhostname.com:5080/frontend/webfrontendConnectionData', 'http://localhost:80/frontend/webfrontendConnectionData']
  tryLocation(locationsToTry.reverse(), callback)
}

export default getData
