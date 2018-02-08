// Dummy file used for testing
//  this will supply the connection information the webfrontend requires to connect to the API backend
//  if the API is fronted by Kong with a security configuration this file will be used by
//  the front end to prompt the user for relevant credentials
//  this file is provided by the API backend server in real environments
//  so that it can supply custom variables to the webfrontend application

export default {
  version: 'Development', // Version show as 0 fom this file
  apiurl: 'http://localhost:80/dockjobapi',
  apiaccesssecurity: [] // all supported auth types. Can be empty, or strings: basic-auth, jwt
  // Empty list means no auth type
  //  { type: basic-auth } - webfrontend will prompt user for username and password
  //  ...
}
