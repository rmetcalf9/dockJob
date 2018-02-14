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
      callback.ok({ data: {
        version: 'Development', // Version show as 0 fom this file
        // TODO PUT BACK apiurl: 'http://localhost:80/dockjobapi',
        apiurl: 'http://somefunnyhostname.com:5080/dockjobapi',
        apiaccesssecurity: [{ type: 'basic-auth' }] // all supported auth types. Can be empty, or JSON: basic-auth, jwt
        // Empty list means no auth type
        //  { type: 'basic-auth' } - webfrontend will prompt user for username and password
        //  ...
      }})
    }
  )
}

export default getData
