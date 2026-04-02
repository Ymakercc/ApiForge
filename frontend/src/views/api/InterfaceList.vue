<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import {
  createInterfaceApi,
  deleteInterfaceApi,
  getInterfaceDetailApi,
  getInterfaceListApi,
  updateInterfaceApi,
  updateInterfaceStatusApi,
  type InterfaceItem,
} from '@/api/interface'

interface SearchForm {
  keyword: string
}

interface InterfaceFormModel {
  name: string
  description: string
  method: string
  url: string
  category: string
  auth_type: string
  is_enabled: number
}

const methodOptions = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
const authTypeOptions = ['none', 'bearer', 'basic', 'apikey']

const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const currentId = ref<number | null>(null)
const tableData = ref<InterfaceItem[]>([])
const formRef = ref<FormInstance>()
const statusLoadingMap = reactive<Record<number, boolean>>({})

const searchForm = reactive<SearchForm>({
  keyword: '',
})

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
})

const form = reactive<InterfaceFormModel>({
  name: '',
  description: '',
  method: 'GET',
  url: '',
  category: '',
  auth_type: 'none',
  is_enabled: 1,
})

const rules: FormRules<InterfaceFormModel> = {
  name: [{ required: true, message: '请输入接口名称', trigger: 'blur' }],
  method: [{ required: true, message: '请选择请求方法', trigger: 'change' }],
  url: [{ required: true, message: '请输入接口地址', trigger: 'blur' }],
}

function resetForm() {
  currentId.value = null
  form.name = ''
  form.description = ''
  form.method = 'GET'
  form.url = ''
  form.category = ''
  form.auth_type = 'none'
  form.is_enabled = 1
}

function buildCreatePayload() {
  return {
    name: form.name.trim(),
    description: form.description.trim() || null,
    method: form.method,
    url: form.url.trim(),
    category: form.category.trim() || null,
    auth_type: form.auth_type,
    is_enabled: form.is_enabled,
  }
}

function buildUpdatePayload() {
  return {
    name: form.name.trim(),
    description: form.description.trim() || null,
    method: form.method,
    url: form.url.trim(),
    category: form.category.trim() || null,
    auth_type: form.auth_type,
  }
}

function getMethodTagType(method: string) {
  const map: Record<string, '' | 'success' | 'warning' | 'danger' | 'info' | 'primary'> = {
    GET: 'success',
    POST: 'primary',
    PUT: 'warning',
    PATCH: 'info',
    DELETE: 'danger',
  }

  return map[method] || 'info'
}

function formatDateTime(value: string) {
  if (!value) {
    return '-'
  }

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }

  return date.toLocaleString()
}

async function fetchList() {
  loading.value = true

  try {
    const data = await getInterfaceListApi({
      page: pagination.page,
      page_size: pagination.pageSize,
      keyword: searchForm.keyword.trim() || undefined,
    })

    tableData.value = data.items
    pagination.total = data.total
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  pagination.page = 1
  fetchList()
}

function handleReset() {
  searchForm.keyword = ''
  pagination.page = 1
  fetchList()
}

function handleAdd() {
  dialogMode.value = 'create'
  resetForm()
  dialogVisible.value = true
}

async function handleEdit(row: InterfaceItem) {
  dialogMode.value = 'edit'
  resetForm()

  try {
    const data = await getInterfaceDetailApi(row.id)
    currentId.value = data.id
    form.name = data.name
    form.description = data.description || ''
    form.method = data.method
    form.url = data.url
    form.category = data.category || ''
    form.auth_type = data.auth_type || 'none'
    form.is_enabled = data.is_enabled
    dialogVisible.value = true
  } catch (error: any) {
    ElMessage.error(error?.response?.data?.detail || '获取接口详情失败')
  }
}

async function handleSubmit() {
  if (!formRef.value) {
    return
  }

  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }

  submitLoading.value = true

  try {
    if (dialogMode.value === 'create') {
      await createInterfaceApi(buildCreatePayload())
      ElMessage.success('接口创建成功')
    } else if (currentId.value) {
      await updateInterfaceApi(currentId.value, buildUpdatePayload())
      ElMessage.success('接口更新成功')
    }

    dialogVisible.value = false
    await fetchList()
  } catch (error: any) {
    ElMessage.error(error?.response?.data?.detail || '保存接口失败')
  } finally {
    submitLoading.value = false
  }
}

async function handleDelete(row: InterfaceItem) {
  try {
    await ElMessageBox.confirm(`确认删除接口“${row.name}”吗？`, '删除确认', {
      type: 'warning',
    })

    await deleteInterfaceApi(row.id)
    ElMessage.success('接口删除成功')

    if (tableData.value.length === 1 && pagination.page > 1) {
      pagination.page -= 1
    }

    await fetchList()
  } catch (error: any) {
    if (error !== 'cancel' && error !== 'close') {
      ElMessage.error(error?.response?.data?.detail || '删除接口失败')
    }
  }
}

async function handleStatusChange(row: InterfaceItem) {
  const value = row.is_enabled
  const previous = value === 1 ? 0 : 1
  statusLoadingMap[row.id] = true

  try {
    const data = await updateInterfaceStatusApi(row.id, value)
    row.is_enabled = data.is_enabled
    ElMessage.success(data.is_enabled === 1 ? '接口已启用' : '接口已禁用')
  } catch (error: any) {
    row.is_enabled = previous
    ElMessage.error(error?.response?.data?.detail || '状态更新失败')
  } finally {
    statusLoadingMap[row.id] = false
  }
}

function handleCurrentChange(page: number) {
  pagination.page = page
  fetchList()
}

function handleSizeChange(size: number) {
  pagination.pageSize = size
  pagination.page = 1
  fetchList()
}

function handleDialogClosed() {
  formRef.value?.clearValidate()
  resetForm()
}

onMounted(() => {
  fetchList()
})
</script>

<template>
  <div class="interface-list-page">
    <el-card shadow="never" class="search-card">
      <el-form :model="searchForm" inline @submit.prevent="handleSearch">
        <el-form-item label="关键字">
          <el-input
            v-model="searchForm.keyword"
            placeholder="按接口名称或地址搜索"
            clearable
            style="width: 280px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <template #header>
        <div class="table-header">
          <span class="card-title">接口列表</span>
          <el-button type="primary" @click="handleAdd">新增接口</el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" row-key="id">
        <el-table-column prop="name" label="接口名称" min-width="180" />
        <el-table-column label="方法" width="110">
          <template #default="{ row }">
            <el-tag :type="getMethodTagType(row.method)">{{ row.method }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="url" label="接口地址" min-width="260" show-overflow-tooltip />
        <el-table-column prop="category" label="分类" min-width="140" />
        <el-table-column label="状态" width="160">
          <template #default="{ row }">
            <el-switch
              v-model="row.is_enabled"
              :active-value="1"
              :inactive-value="0"
              :loading="!!statusLoadingMap[row.id]"
              inline-prompt
              active-text="启用"
              inactive-text="禁用"
              @change="handleStatusChange(row)"
            />
          </template>
        </el-table-column>
        <el-table-column label="更新时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.updated_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
        <template #empty>
          <el-empty description="暂无接口数据" />
        </template>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          background
          layout="total, sizes, prev, pager, next, jumper"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          @current-change="handleCurrentChange"
          @size-change="handleSizeChange"
        />
      </div>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'create' ? '新增接口' : '编辑接口'"
      width="640px"
      destroy-on-close
      @closed="handleDialogClosed"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="接口名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入接口名称" />
        </el-form-item>

        <el-form-item label="请求方法" prop="method">
          <el-select v-model="form.method" placeholder="请选择请求方法" style="width: 100%">
            <el-option v-for="item in methodOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>

        <el-form-item label="接口地址" prop="url">
          <el-input v-model="form.url" placeholder="请输入接口地址，例如 https://api.example.com/users" />
        </el-form-item>

        <el-form-item label="分类">
          <el-input v-model="form.category" placeholder="请输入接口分类" />
        </el-form-item>

        <el-form-item label="认证类型">
          <el-select v-model="form.auth_type" placeholder="请选择认证类型" style="width: 100%">
            <el-option v-for="item in authTypeOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>

        <el-form-item v-if="dialogMode === 'create'" label="默认状态">
          <el-switch v-model="form.is_enabled" :active-value="1" :inactive-value="0" inline-prompt active-text="启用" inactive-text="禁用" />
        </el-form-item>

        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入接口说明" />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="submitLoading" @click="handleSubmit">
            {{ dialogMode === 'create' ? '创建' : '保存' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.interface-list-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.search-card :deep(.el-card__body) {
  padding-bottom: 4px;
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>
