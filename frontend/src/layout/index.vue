<script setup lang="ts">
import Sidebar from './Sidebar.vue'
import Topbar from './Topbar.vue'
</script>

<template>
  <el-container class="app-wrapper">
    <el-aside width="220px">
      <Sidebar />
    </el-aside>
    <el-container>
      <el-header height="60px" style="padding: 0;">
        <Topbar />
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.app-wrapper {
  height: 100vh;
  overflow: hidden;
}

.el-aside {
  overflow: hidden;
}

.el-main {
  background: #f5f7fa;
  overflow-y: auto;
  padding: 24px;
}
</style>
