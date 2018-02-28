import Vue from 'vue'
import VueRouter from 'vue-router'
import globalStore from './stores/globalStore'
// import callbackHelper from 'callbackHelper'

Vue.use(VueRouter)

function defaultBeforeNavFn (to, from, next, pageTitle) {
  globalStore.commit('SET_PAGE_TITLE', pageTitle)
  next()
}

// Function to implement a commonPreLoad depending on the dataStore state
// INITIAL -> Go to login page, which will query server info and find out if login is required
// REQUIRE_LOGIN -> Go to login page and prompt user to log in
// LOGGED_IN -> Go to requested page
function commonPreLoad (to, from, next) {
  if ((globalStore.getters.datastoreState === 'LOGGED_IN') || (globalStore.getters.datastoreState === 'LOGGED_IN_SERVERDATA_LOADED')) {
    next()
    return
  }
  next({
    path: '/login',
    query: { redirect: to.fullPath }
  })
}

function load (component) {
  // '@' is aliased to src/components
  return () => import(`@/${component}.vue`)
}

export default new VueRouter({
  /*
   * NOTE! VueRouter "history" mode DOESN'T works for Cordova builds,
   * it is only to be used only for websites.
   *
   * If you decide to go with "history" mode, please also open /config/index.js
   * and set "build.publicPath" to something other than an empty string.
   * Example: '/' instead of current ''
   *
   * If switching back to default "hash" mode, don't forget to set the
   * build publicPath back to '' so Cordova builds work again.
   */

  mode: 'hash',
  scrollBehavior: () => ({ y: 0 }),

  routes: [
    {
      path: '/',
      component: load('Index'),
      beforeEnter: commonPreLoad,
      children: [
        { path: '/', redirect: '/dashboard' },
        { path: 'dashboard', component: load('Dashboard'), beforeEnter (to, from, next) { defaultBeforeNavFn(to, from, next, 'Dashboard') } },
        { path: 'jobs', component: load('Jobs'), beforeEnter (to, from, next) { defaultBeforeNavFn(to, from, next, 'Jobs') } }
      ]
    },
    { path: '/login', component: load('Login') }, // Can't redirect to common preload or we will get endless loop
    { path: '/logout',
      beforeEnter (to, from, next) {
        var callback = {
          ok: function (response) {
            console.log(globalStore.getters.datastoreState)
            next('/login')
          },
          error: function (response) {
            console.log(response.message)
          }
        }
        globalStore.dispatch('logout', {callback: callback})
      }
    },
    // Always leave this last one
    { path: '*', component: load('Error404') } // Not found
  ]
})
