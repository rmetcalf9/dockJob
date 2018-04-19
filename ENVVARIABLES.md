# Enviroment variable configuration detail

This application is based on baseapp_for_restapi_backend_with_swagger so enviroment variables from that project can be used. They are documented [here](https://github.com/rmetcalf9/baseapp_for_restapi_backend_with_swagger/blob/master/docs/ENVVARIABLES.md).

## Extra variables added

 | Name | Example Value | Meaning |
 | ---- | ------------- | ------- |
 | APIAPP_USERFORJOBS | dockjobuser | OS user used for running jobs. |
 | APIAPP_GROUPFORJOBS | dockjobgroup | OS group used for running jobs. |
 | APIAPP_SKIPUSERCHECK | False | If set to false the application will check it has permission to run a job with the named user and group. This slows down test execution so this option was added to disable it. |

## APIAPP_APIACCESSSECURITY
APIAPP_APIACCESSSECURITY must be valid JSON representing the way the frontend should obtain credentials to call the API's. This is required as a variable to respect different Kong configurations.

 | Value | Meaning |
 | ---- | ------------- |
 | [] | An empty array means that no authroization is needed to call the API's. |
 | [ { type: 'basic-auth' } ] | Basic auth means the user should be prompted for a username and password and this added to API calls as a basic authroization header. |
 | [ { type: 'basic-auth-login-toget-jwttoken', loginurl: 'https://x/login/', cookiename: 'jwt-auth-cookie' } ] | Call a login endpoint to get a JWT token which is then supplied to the API's as a cookie |

## Docker container helper variables

 | Name | Example Value | Meaning |
 | ---- | ------------- | ------- |
 | DOCKERRUN_USERHOSTFILE | /run/secrets/webservices_hostname | This points to a file inside the container; probally supplied as a secret or config. If this variable is present the file is read into the contents of an enviroment variable 'DOCKERRUN_USERHOST'. All other enviroment variables starting with APIAPP_ can refer to DOCKERRUN_USERHOST. (If specifying in docker compose files preceed with two $'s.)  |

