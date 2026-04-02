<script setup lang="ts">
import { ref } from 'vue'

const search = ref('')
const templates: any[] = []
</script>

<template>
  <el-card shadow="never">
    <template #header>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span>Skill 模板库</span>
        <el-input v-model="search" placeholder="搜索模板..." prefix-icon="Search" style="width: 240px;" />
      </div>
    </template>
    <el-row :gutter="16">
      <el-col v-if="templates.length === 0" :span="24">
        <el-empty description="暂无 Skill 模板" />
      </el-col>
      <el-col v-for="tpl in templates" :key="tpl.id" :span="8">
        <el-card shadow="hover" class="tpl-card">
          <h3>{{ tpl.name }}</h3>
          <p>{{ tpl.description }}</p>
          <el-button size="small" type="primary">使用模板</el-button>
        </el-card>
      </el-col>
    </el-row>
  </el-card>
</template>

<style scoped>
.tpl-card {
  margin-bottom: 16px;
  cursor: pointer;
}
</style>
