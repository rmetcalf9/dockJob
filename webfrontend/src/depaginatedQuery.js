// Provides function that runs a query and calls service mutiple times returning a full list of results
import restcallutils from './restcallutils'

var GpageSize = 25
var GmaxPages = 15

function getDepaginatedQueryResults (basePath, queryParamArr, finalCallback, apiFN) {
  _getDepaginatedQueryResults(basePath, queryParamArr, finalCallback, apiFN, 0, 0, [], GpageSize)
}

function _getDepaginatedQueryResults (basePath, queryParamArr, finalCallback, apiFN, offset, pagesSoFar, resultsSoFar, pageSize) {
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
        _getDepaginatedQueryResults(basePath, queryParamArr, finalCallback, apiFN, nextOffset, pagesSoFar + 1, nextResultsSoFar, response.data.pagination.pagesize)
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
  apiFN('GET', restcallutils.buildQueryString(basePath, queryParamArr), undefined, callback)
}

export default {
  getDepaginatedQueryResults: getDepaginatedQueryResults
}
