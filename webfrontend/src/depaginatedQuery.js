// Provides function that runs a query and calls service mutiple times returning a full list of results

function getDepaginatedQueryResults (queryString, finalCallback, apiFN) {
  var callback = finalCallback

  apiFN('GET', queryString, undefined, callback)
}

export default {
  getDepaginatedQueryResults: getDepaginatedQueryResults
}
