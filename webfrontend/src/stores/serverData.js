// Dummy file used for testing
//  this file is provided by dockjobapi server in real enviroments
//  so that it can supply custom variables to the webfrontend application

export default {
  version: 'Development', // Version show as 0 fom this file
  apiurl: 'http://localhost:80/dockjobapi',
  apiaccesssecurity: [] // all supported auth types. Can be empty, or strings: basic-auth, jwt
}
