import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: HomeView },
    { path: '/pre-open', component: () => import('../views/PreOpenView.vue') },
    { path: '/operations', component: () => import('../views/OperationsView.vue') },
    { path: '/marketing', component: () => import('../views/MarketingView.vue') },
    { path: '/finance', component: () => import('../views/FinanceView.vue') },
    { path: '/faq', component: () => import('../views/FaqView.vue') },
    { path: '/support', component: () => import('../views/SupportView.vue') },
    { path: '/education', component: () => import('../views/EducationView.vue') },
  ],
})

export default router
