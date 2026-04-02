import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const WHITE_LIST = new Set(['/login'])

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/login/index.vue'),
      meta: { public: true },
    },
    {
      path: '/',
      component: () => import('@/layout/index.vue'),
      redirect: '/dashboard',
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: () => import('@/views/dashboard/index.vue'),
          meta: { title: '仪表盘', icon: 'Odometer' },
        },
        {
          path: 'api',
          name: 'ApiManagement',
          component: () => import('@/views/api/index.vue'),
          meta: { title: '接口管理', icon: 'Grid' },
        },
        {
          path: 'debug',
          name: 'ApiDebug',
          component: () => import('@/views/debug/index.vue'),
          meta: { title: '接口调试', icon: 'Monitor' },
        },
        {
          path: 'logs',
          name: 'Logs',
          component: () => import('@/views/logs/index.vue'),
          meta: { title: '日志', icon: 'Document' },
        },
        {
          path: 'skill-templates',
          name: 'SkillTemplates',
          component: () => import('@/views/skill-templates/index.vue'),
          meta: { title: 'Skill 模板', icon: 'Collection' },
        },
        {
          path: 'skill-generator',
          name: 'SkillGenerator',
          component: () => import('@/views/skill-generator/index.vue'),
          meta: { title: 'Skill 生成', icon: 'MagicStick' },
        },
        {
          path: 'settings',
          name: 'Settings',
          component: () => import('@/views/settings/index.vue'),
          meta: { title: '系统设置', icon: 'Setting' },
        },
      ],
    },
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
})

router.beforeEach(async (to) => {
  const userStore = useUserStore()
  const hasToken = !!userStore.token
  const isWhiteListed = WHITE_LIST.has(to.path) || !!to.meta.public

  if (!hasToken && !isWhiteListed) {
    return {
      name: 'Login',
      query: { redirect: to.fullPath },
    }
  }

  if (to.name === 'Login' && hasToken) {
    return { name: 'Dashboard' }
  }

  if (hasToken && !userStore.userInfo && !isWhiteListed) {
    try {
      await userStore.fetchUserInfo()
    } catch {
      return {
        name: 'Login',
        query: { redirect: to.fullPath },
      }
    }
  }
})

export default router
