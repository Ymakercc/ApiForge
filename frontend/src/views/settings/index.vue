<script setup lang="ts">
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'

const form = reactive({
  apiBaseUrl: 'http://localhost:8020',
  defaultModel: 'claude-sonnet-4-6',
  logLevel: 'INFO',
  maxRetries: 3,
})

function save() {
  ElMessage.success('设置已保存')
}
</script>

<template>
  <el-card shadow="never" style="max-width: 640px;">
    <template #header>系统设置</template>
    <el-form :model="form" label-width="120px">
      <el-form-item label="后端地址">
        <el-input v-model="form.apiBaseUrl" />
      </el-form-item>
      <el-form-item label="默认模型">
        <el-select v-model="form.defaultModel" style="width: 100%;">
          <el-option label="claude-sonnet-4-6" value="claude-sonnet-4-6" />
          <el-option label="claude-opus-4-6" value="claude-opus-4-6" />
          <el-option label="claude-haiku-4-5-20251001" value="claude-haiku-4-5-20251001" />
        </el-select>
      </el-form-item>
      <el-form-item label="日志级别">
        <el-select v-model="form.logLevel" style="width: 100%;">
          <el-option label="DEBUG" value="DEBUG" />
          <el-option label="INFO" value="INFO" />
          <el-option label="WARN" value="WARN" />
          <el-option label="ERROR" value="ERROR" />
        </el-select>
      </el-form-item>
      <el-form-item label="最大重试次数">
        <el-input-number v-model="form.maxRetries" :min="0" :max="10" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="save">保存</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>
