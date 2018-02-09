// This class contains functions to help callbacks

function callbackWithError (callback, msg, obj) {
  var retobj = {
    message: msg,
    orig: obj
  }
  console.log(retobj)
  callback.error(retobj)
}
function callbackWithSimpleError (callback, msg) {
  callbackWithError(callback, msg, undefined)
}
function callbackWithNotImplemented (callback) {
  callbackWithError(callback, 'Not Implemented', undefined)
}

export default {
  callbackWithError: callbackWithError,
  callbackWithSimpleError: callbackWithSimpleError,
  callbackWithNotImplemented: callbackWithNotImplemented
}
