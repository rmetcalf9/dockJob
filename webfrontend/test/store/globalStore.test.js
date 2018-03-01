// globalStore tests
import commonUtils from '../commonUtils.js'
const store = require('../../src/store/globalStore.js')
const globalStore = store.default
import callbackHelper from '../../src/callbackHelper'
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
  //mocking callDockjobAPI (apiurl, dockJobAccessCredentials, method, pathWithoutStartingSlash, postdata, callback)
  const accessCredentials = {a: 'TEST'}
  const sucessfulGetServerinfoCall = jest.fn(function (apiurl, dockJobAccessCredentials, method, pathWithoutStartingSlash, postdata, callback) {
    expect(method).toBe('GET');
    expect(pathWithoutStartingSlash).toBe('serverinfo/');
    expect(dockJobAccessCredentials).toBe(accessCredentials);
    callback.ok({
      status: 200,
      statusText: 'OK',
      data: {
        Jobs: {NextExecuteJob: undefined, TotalJobs: 0},
        Server: {NextExecuteJob: 'Europe/London', ServerDatetime: '2018-02-12 18:29:31.554385+00:00'}
      }
    })
  })

  store.mutations.SET_APIFN(gsState, sucessfulGetServerinfoCall)

  var callback = {
    ok: function (response) {
      expect(gsState.datastoreState).toBe('LOGGED_IN_SERVERDATA_LOADED');
      done()
    },
    error: function (response) {
      done.fail(new Error('Should not report failed login'))
    }
  }
  store.actions.login({commit: commonUtils.getCommitFN(gsState, store.mutations), state: gsState}, {callback: callback, accessCredentials: accessCredentials})
});

test('Login basic-auth fail', done => {
  var gsState = store.getInitialState()
  expect(gsState.datastoreState).toBe('INITIAL');
  
  store.mutations.SET_CONNECTIONDATA(gsState, {'version': 'TEST','apiurl': 'https://test','apiaccesssecurity': [{'type': 'basic-auth' }]})
  expect(gsState.datastoreState).toBe('REQUIRE_LOGIN');

  // Mock the API function so we can control it's response
  //mocking callDockjobAPI (apiurl, dockJobAccessCredentials, method, pathWithoutStartingSlash, postdata, callback)
  const accessCredentials = {a: 'TEST'}
  const sucessfulGetServerinfoCall = jest.fn(function (apiurl, dockJobAccessCredentials, method, pathWithoutStartingSlash, postdata, callback) {
    expect(method).toBe('GET')
    expect(pathWithoutStartingSlash).toBe('serverinfo/')
    expect(dockJobAccessCredentials).toBe(accessCredentials)
    callbackHelper.webserviceError(callback, {
      status: 500,
      statusText: 'ERROR',
      message: 'TEST ERROR MSG'
    })
  })

  store.mutations.SET_APIFN(gsState, sucessfulGetServerinfoCall)

  var callback = {
    ok: function (response) {
      done.fail(new Error('Should not report sucessful login'))
    },
    error: function (response) {
      expect(gsState.datastoreState).toBe('REQUIRE_LOGIN');
      done()
    }
  }
  store.actions.login({commit: commonUtils.getCommitFN(gsState, store.mutations), state: gsState}, {callback: callback, accessCredentials: accessCredentials})
});

test('Login and logout basic-auth success', done => {
  var gsState = store.getInitialState()
  expect(gsState.datastoreState).toBe('INITIAL');
  
  store.mutations.SET_CONNECTIONDATA(gsState, {'version': 'TEST','apiurl': 'https://test','apiaccesssecurity': [{'type': 'basic-auth' }]})
  expect(gsState.datastoreState).toBe('REQUIRE_LOGIN');

  // Mock the API function so we can control it's response
  //mocking callDockjobAPI (apiurl, dockJobAccessCredentials, method, pathWithoutStartingSlash, postdata, callback)
  const accessCredentials = {a: 'TEST'}
  const sucessfulGetServerinfoCall = jest.fn(function (apiurl, dockJobAccessCredentials, method, pathWithoutStartingSlash, postdata, callback) {
    expect(method).toBe('GET');
    expect(pathWithoutStartingSlash).toBe('serverinfo/');
    expect(dockJobAccessCredentials).toBe(accessCredentials);
    callback.ok({
      status: 200,
      statusText: 'OK',
      data: {
        Jobs: {NextExecuteJob: undefined, TotalJobs: 0},
        Server: {NextExecuteJob: 'Europe/London', ServerDatetime: '2018-02-12 18:29:31.554385+00:00'}
      }
    })
  })

  store.mutations.SET_APIFN(gsState, sucessfulGetServerinfoCall)

  var callback = {
    ok: function (response) {
      var callback2 = {
        ok: function (response) {
          expect(gsState.datastoreState).toBe('REQUIRE_LOGIN');
          expect(gsState.accessCredentials).toBeUndefined();
          done()
        },
        error: function (response) {
          done.fail(new Error('Logout should not fail'))
        }
      }
      expect(gsState.datastoreState).toBe('LOGGED_IN_SERVERDATA_LOADED')
  
      store.actions.logout({commit: commonUtils.getCommitFN(gsState, store.mutations), state: gsState}, {callback: callback2})
    },
    error: function (response) {
      done.fail(new Error('Should not report failed login'))
    }
  }
  store.actions.login({commit: commonUtils.getCommitFN(gsState, store.mutations), state: gsState}, {callback: callback, accessCredentials: accessCredentials})
});

