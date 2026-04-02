<script setup lang="ts">
import { reactive, ref } from 'vue'

const form = reactive({
  apiId: '',
  skillName: '',
  description: '',
  model: 'claude-sonnet-4-6',
})
const generated = ref('')
const loading = ref(false)

const models = ['claude-sonnet-4-6', 'claude-opus-4-6', 'claude-haiku-4-5-20251001']

async function generate() {
  loading.value = true
  generated.value = ''
  try {
    await new Promise((r) => setTimeout(r, 800))
    generated.value = `# ${form.skillName || 'Generated Skill'}\n\n// TODO: 生成结果将显示在此处`
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <el-row :gutter="16">
    <el-col :span="10">
      <el-card shadow="never" header="生成配置">
        <el-form label-width="90px">
          <el-form-item label="接口">
            <el-input v-model="form.apiId" placeholder="选择或输入接口 ID" />
          </el-form-item>
          <el-form-item label="Skill 名称">
            <el-input v-model="form.skillName" placeholder="my_skill" />
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="form.description" type="textarea" :rows="3" placeholder="描述 Skill 的用途..." />
          </el-form-item>
          <el-form-item label="模型">
            <el-select v-model="form.model" style="width: 100%;">
              <el-option v-for="m in models" :key="m" :label="m" :value="m" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="loading" @click="generate">生成 Skill</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-col>
    <el-col :span="14">
      <el-card shadow="never" header="生成结果">
        <pre class="code-output">{{ generated || '配置后点击生成...' }}</pre>
        <div v-if="generated" style="margin-top: 12px; display: flex; gap: 8px;">
          <el-button size="small" icon="Download">导出</el-button>
          <el-button size="small" icon="CopyDocument">复制</el-button>
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>

<style scoped>
.code-output {
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
