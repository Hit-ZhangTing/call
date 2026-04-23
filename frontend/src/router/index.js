import { createRouter, createWebHashHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/register', component: Register },
  { path: '/dashboard', component: Dashboard }
]

const router = createRouter({ history: createWebHashHistory(), routes })

export default router
