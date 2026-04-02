<script setup lang="ts">
import { useRoute } from 'vue-router'
import * as Icons from '@element-plus/icons-vue'
import { computed, defineComponent, h } from 'vue'

const route = useRoute()

const menus = [
  { path: '/dashboard',        title: '仪表盘',    icon: 'Odometer' },
  { path: '/api',              title: '接口管理',  icon: 'Grid' },
  { path: '/debug',            title: '接口调试',  icon: 'Monitor' },
  { path: '/logs',             title: '日志',      icon: 'Document' },
  { path: '/skill-templates',  title: 'Skill 模板', icon: 'Collection' },
  { path: '/skill-generator',  title: 'Skill 生成', icon: 'MagicStick' },
  { path: '/settings',         title: '系统设置',  icon: 'Setting' },
]

const activeMenu = computed(() => route.path)

function renderIcon(name: string) {
  const comp = (Icons as any)[name]
  return comp ? defineComponent({ render: () => h(comp) }) : null
}
</script>

<template>
  <div class="sidebar">
    <div class="logo">
      <span class="logo-text">ApiForge</span>
    </div>
    <el-menu
      :default-active="activeMenu"
      router
      background-color="#1e1e2e"
      text-color="#cdd6f4"
      active-text-color="#89b4fa"
    >
      <el-menu-item v-for="item in menus" :key="item.path" :index="item.path">
        <el-icon v-if="renderIcon(item.icon)">
          <component :is="renderIcon(item.icon)" />
        </el-icon>
        <span>{{ item.title }}</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<style scoped>
.sidebar {
  height: 100%;
  background: #1e1e2e;
  display: flex;
  flex-direction: column;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #313244;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: #89b4fa;
  letter-spacing: 2px;
}

.el-menu {
  border-right: none;
  flex: 1;
}
</style>
