import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: HomeView },
    { path: '/education', component: () => import('../views/EducationView.vue') },
    { path: '/pre-open', component: () => import('../views/PreOpenView.vue') },
    { path: '/operations', component: () => import('../views/OperationsView.vue') },
    { path: '/marketing', component: () => import('../views/MarketingView.vue') },
    { path: '/finance', component: () => import('../views/FinanceView.vue') },
    { path: '/faq', component: () => import('../views/FaqView.vue') },
    { path: '/support', component: () => import('../views/SupportView.vue') },
    { path: '/startup', component: () => import('../views/startup/StartupDashboardView.vue') },
    { path: '/startup/checklist', component: () => import('../views/startup/ChecklistView.vue') },
    { path: '/startup/properties', component: () => import('../views/startup/PropertyCompareView.vue') },
    { path: '/startup/properties/new', component: () => import('../views/startup/PropertyFormView.vue') },
    { path: '/startup/properties/:id', component: () => import('../views/startup/PropertyFormView.vue') },
    { path: '/startup/market', component: () => import('../views/startup/MarketAnalysisView.vue') },
    { path: '/startup/evidence', component: () => import('../views/startup/EvidenceView.vue') },
  ],
})

export default router
