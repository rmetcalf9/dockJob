// Provides function that runs a query and calls service mutiple times returning a full list of results
import restcallutils from './restcallutils'

var GpageSize = 25
var GmaxPages = 15

function getDepaginatedQueryResults (basePath, queryParamArr, finalCallback, wrappedCallApiFn) {
  _getDepaginatedQueryResults(basePath, queryParamArr, finalCallback, wrappedCallApiFn, 0, 0, [], GpageSize)
}

function _getDepaginatedQueryResults (basePath, queryParamArr, finalCallback, wrappedCallApiFn, offset, pagesSoFar, resultsSoFar, pageSize) {
  if (pagesSoFar >= GmaxPages) {
    finalCallback.ok({
      data: {
        dePaginatorResp: {
          pagesReturned: pagesSoFar,
          complete: false
        },
        result: resultsSoFar
      }
    })
    return
  }
  var callback = {
    ok: function (response) {
      var nextResultsSoFar = resultsSoFar.concat(response.data.result)
      var nextOffset = response.data.pagination.offset + response.data.pagination.pagesize
      if (nextOffset < response.data.pagination.total) {
        _getDepaginatedQueryResults(basePath, queryParamArr, finalCallback, wrappedCallApiFn, nextOffset, pagesSoFar + 1, nextResultsSoFar, response.data.pagination.pagesize)
        return
      }
      finalCallback.ok({
        data: {
          dePaginatorResp: {
            pagesReturned: pagesSoFar,
            complete: true
          },
          result: nextResultsSoFar
        }
      })
    },
    error: finalCallback.error
  }

  queryParamArr['pagesize'] = pageSize.toString()
  queryParamArr['offset'] = offset.toString()
  wrappedCallApiFn({
    method: 'GET',
    path:  restcallutils.buildQueryString(basePath, queryParamArr),
    postdata: undefined,
    callback
  })
}

export default {
  getDepaginatedQueryResults: getDepaginatedQueryResults
}
