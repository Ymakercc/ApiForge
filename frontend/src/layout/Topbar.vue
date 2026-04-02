<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { computed } from 'vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const pageTitle = computed(() => (route.meta.title as string) || 'ApiForge')

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="topbar">
    <span class="page-title">{{ pageTitle }}</span>
    <div class="topbar-right">
      <el-dropdown @command="handleLogout">
        <span class="user-info">
          <el-icon><UserFilled /></el-icon>
          <span>{{ userStore.userInfo?.username || 'Admin' }}</span>
          <el-icon class="arrow"><ArrowDown /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<style scoped>
.topbar {
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.page-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  color: #606266;
  font-size: 14px;
}

.user-info:hover {
  color: #409eff;
}

.arrow {
  font-size: 12px;
}
</style>
