<script setup lang="ts">
import { reactive, ref } from 'vue'

const form = reactive({
  method: 'GET',
  url: '',
  headers: '',
  body: '',
})
const response = ref('')
const loading = ref(false)

const methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

async function send() {
  if (!form.url) return
  loading.value = true
  response.value = ''
  try {
    // TODO: proxy via backend
    response.value = JSON.stringify({ message: '功能开发中，请通过后端代理发送请求' }, null, 2)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <el-row :gutter="16">
    <el-col :span="12">
      <el-card shadow="never" header="请求">
        <el-form label-width="60px">
          <el-form-item label="方法">
            <el-select v-model="form.method" style="width: 120px;">
              <el-option v-for="m in methods" :key="m" :label="m" :value="m" />
            </el-select>
          </el-form-item>
          <el-form-item label="URL">
            <el-input v-model="form.url" placeholder="https://..." />
          </el-form-item>
          <el-form-item label="Headers">
            <el-input v-model="form.headers" type="textarea" :rows="4" placeholder='{"Content-Type": "application/json"}' />
          </el-form-item>
          <el-form-item label="Body">
            <el-input v-model="form.body" type="textarea" :rows="6" placeholder='{"key": "value"}' />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="loading" @click="send">发送</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-col>
    <el-col :span="12">
      <el-card shadow="never" header="响应">
        <pre class="response-body">{{ response || '等待发送...' }}</pre>
      </el-card>
    </el-col>
  </el-row>
</template>

<style scoped>
.response-body {
  background: #1e1e2e;
  color: #cdd6f4;
  border-radius: 6px;
  padding: 16px;
  font-size: 13px;
  min-height: 320px;
  overflow: auto;
  white-space: pre-wrap;
  word-break: break-all;
}
</style>
