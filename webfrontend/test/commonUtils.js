// Common code used in all tests



export default {
  getCommitFN: function (state, mutations) {
    return function (mutationFnName, params) {
      var fn = mutations[mutationFnName]
      return fn(state, params)
    }
  }
}
