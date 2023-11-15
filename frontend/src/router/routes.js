
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', redirect: '/dashboard' },
      { path: '/dashboard', component: () => import('pages/Dashboard.vue') },
      { path: '/executions', component: () => import('pages/Executions.vue') },
      { path: '/executions/:executionGUID', component: () => import('pages/Execution.vue') },
      { path: '/jobs', component: () => import('pages/Jobs.vue') },
      { path: '/jobs/:jobGUID', component: () => import('pages/Job.vue') }
    ]
  },
  {
    path: '/login',
    component: () => import('pages/Login.vue')
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
