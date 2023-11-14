// This class contains functions to help when calling rest services

function insertString (sofar, name, value) {
  if (sofar.length === 0) {
    sofar = sofar + '?'
  } else {
    sofar = sofar + '&'
  }
  return sofar + name + '=' + value
}

function buildQueryString (prefix, params) {
  if (typeof (params) === 'undefined') {
    return prefix
  }
  var str = ''
  // opted against this method because it allows mutiple values for same key
  // params.map(function (item) {
  //  str = insertString(str, item.name, item.value)
  // })
  for (var x in params) {
    str = insertString(str, x, params[x])
  }
  return prefix + str
}

export default {
  buildQueryString
}
