// globalStore tests
const store = require('../../src/stores/globalStore.js')
const globalStore = store.default
// import globalStore from '../../src/stores/globalStore.js'
// import {getInitialState, mutations, actions} from '../../src/stores/globalStore.js'

test('Start state is INITIAL', () => {
  var gsState = store.getInitialState()
  expect(gsState.datastoreState).toBe('INITIAL');
});
test('Setting connection data with no loginmodes changes state to LOGGED_IN', () => {
  var gsState = store.getInitialState()
  store.mutations.SET_CONNECTIONDATA(gsState, {'version': 'TEST','apiurl': 'https://test','apiaccesssecurity': []})
  expect(gsState.datastoreState).toBe('LOGGED_IN');
});
test('Setting connection data with basic-auth login mode changes state to REQUIRE_LOGIN', () => {
  var gsState = store.getInitialState()
  store.mutations.SET_CONNECTIONDATA(gsState, {'version': 'TEST','apiurl': 'https://test','apiaccesssecurity': [{'type': 'basic-auth' }]})
  expect(gsState.datastoreState).toBe('REQUIRE_LOGIN');
});


  
/*        var callback = {
        ok: function (response) {
          Loading.hide()
          TTT.$router.replace(TTT.$route.query.redirect || '/')
        },
        error: function (response) {
          Loading.hide()
          Toast.create(response.message)
        }
      }
      globalStore.dispatch('init', {callback: callback})
  */
