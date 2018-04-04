const utility = require('../src/restcallutils.js')

/*
test('buildSampleQueryString', () => {
  expect(utility.default.buildQueryString('/jobs',undefined)).toBe('/jobs')
  expect(utility.default.buildQueryString('/jobs',[])).toBe('/jobs')
  expect(utility.default.buildQueryString('/jobs',[{name: 'P1', value: 'P1Val'}])).toBe('/jobs?P1=P1Val')
  expect(utility.default.buildQueryString('/jobs',[{name: 'P1', value: 'P1Val'}, {name: 'P2', value: 'P2Val'}])).toBe('/jobs?P1=P1Val&P2=P2Val')
  
  var tt = []
  tt.push({name: 'P1', value:'V1'})
  expect(utility.default.buildQueryString('/jobs',tt)).toBe('/jobs?P1=V1')
})
*/

test('buildSampleQueryStringFromArray', () => {
  var sec = []
  sec['P1']='V1'
  expect(utility.default.buildQueryString('/jobs',sec)).toBe('/jobs?P1=V1')
})