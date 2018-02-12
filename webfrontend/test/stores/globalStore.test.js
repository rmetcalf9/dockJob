// globalStore tests
import commonUtils from '../commonUtils.js'
const store = require('../../src/stores/globalStore.js')
const globalStore = store.default
// import globalStore from '../../src/stores/globalStore.js'
// import {getInitialState, mutations, actions} from '../../src/stores/globalStore.js'

test('Start state is INITIAL', () => {
  var gsState = store.getInitialState()
  expect(gsState.datastoreState).toBe('INITIAL');
});

// For this test to pass done must be called
//  see https://facebook.github.io/jest/docs/en/asynchronous.html
test('Start init Action', done => {
  var gsState = store.getInitialState()
  expect(gsState.datastoreState).toBe('INITIAL');
  var callback = {
    ok: function (response) {
      expect(gsState.datastoreState).toBe('LOGGED_IN');
      done()
    },
    error: function (response) {
    }
  }
  store.actions.init({commit: commonUtils.getCommitFN(gsState, store.mutations), state: gsState}, {callback: callback})
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

test('Login basic-auth success', done => {
  var gsState = store.getInitialState()
  expect(gsState.datastoreState).toBe('INITIAL');
  
  store.mutations.SET_CONNECTIONDATA(gsState, {'version': 'TEST','apiurl': 'https://test','apiaccesssecurity': [{'type': 'basic-auth' }]})
  expect(gsState.datastoreState).toBe('REQUIRE_LOGIN');

  // Mock the API function so we can control it's response
  store.mutations.SET_APIFN(gsState, function () {console.log('TODO JEST Mock')})


  var callback = {
    ok: function (response) {
      expect(gsState.datastoreState).toBe('LOGGED_IN');
      done()
    },
    error: function (response) {
    }
  }
  store.actions.login({commit: commonUtils.getCommitFN(gsState, store.mutations), state: gsState}, {callback: callback})
});

//TODO Test login fail

//TODO Test logout

