import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  { 
    path: '/', 
    name: 'Home', 
    component: () => import('@/components/Welcome.vue') 
  },
  { 
    path: '/about', 
    name: 'About', 
    component: () => import('@/components/About.vue') 
  },
  { 
    path: '/products', 
    name: 'Products', 
    component: () => import('@/components/entity/product/Products.vue') 
  },
  { 
    path: '/login', 
    name: 'Login', 
    component: () => import('@/components/Login.vue') 
  },
  { 
    path: '/admin/products', 
    name: 'AdminProducts', 
    component: () => import('@/components/admin/AdminProducts.vue'),
    meta: { requiresAdmin: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

