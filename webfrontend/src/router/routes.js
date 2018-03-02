import globalStore from '../store/globalStore'

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

export default [
  {
    path: '/',
    component: () => import('layouts/Index'),
    beforeEnter: commonPreLoad,
    children: [
      { path: '', redirect: '/dashboard' },
      { path: 'dashboard', component: () => import('pages/Dashboard'), beforeEnter (to, from, next) { defaultBeforeNavFn(to, from, next, 'Dashboard') } },
      { path: 'jobs', component: () => import('pages/Jobs'), beforeEnter (to, from, next) { defaultBeforeNavFn(to, from, next, 'Jobs') } }
    ]
  },
  { path: '/login', component: () => import('pages/Login') }, // Can't redirect to common preload or we will get endless loop
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
  { // Always leave this as last one
    path: '*',
    component: () => import('pages/404')
  }
]
