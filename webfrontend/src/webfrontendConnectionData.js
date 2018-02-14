// Retrieve webfrontend connection data
//  If service call returns an error provide static development values
import axios from 'axios'
// import callbackHelper from 'callbackHelper'

function getData (callback) {
  var config = {
    method: 'GET',
    url: 'webfrontendConnectionData'
  }
  axios(config).then(
    (response) => {
      callback.ok(response)
    },
    (response) => {
      var devBoxData = {
        version: 'Development-devBoxData', // Version show as 0 fom this file
        apiurl: 'http://localhost:80/dockjobapi',
        apiaccesssecurity: [] // all supported auth types. Can be empty, or JSON: basic-auth, jwt
        // Empty list means no auth type
        //  { type: 'basic-auth' } - webfrontend will prompt user for username and password
        //  ...
      }
      var basicAuthData = {
        version: 'Development-basicAuthData',
        apiurl: 'http://localhost:80/dockjobapi',
        apiaccesssecurity: [{type: 'basic-auth'}]
      }
      var a = false
      if (a) {
        console.log(devBoxData)
        console.log(basicAuthData)
      }
      callback.ok({data: devBoxData})
    }
  )
}

export default getData
