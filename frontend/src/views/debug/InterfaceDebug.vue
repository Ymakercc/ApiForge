<script setup lang="ts">
import {
  createInterfaceTestCaseApi,
  debugInterfaceApi,
  getInterfaceDetailApi,
  getInterfaceListApi,
  getInterfaceTestCasesApi,
  type InterfaceDebugResponse,
  type InterfaceItem,
  type InterfaceTestCaseItem,
  type JsonObject,
} from "@/api/interface";
import { ElMessage } from "element-plus";
import { computed, onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

interface RequestEditorState {
  headers: string;
  params: string;
  body: string;
}

interface TestCaseFormState {
  name: string;
  description: string;
  expectedStatus: string;
  expectedKeywords: string;
  remark: string;
}

const route = useRoute();
const router = useRouter();

const interfaces = ref<InterfaceItem[]>([]);
const currentInterface = ref<InterfaceItem | null>(null);
const selectedInterfaceId = ref<number | null>(null);
const testCases = ref<InterfaceTestCaseItem[]>([]);
const selectedTestCaseId = ref<number | null>(null);

const loadingInterfaces = ref(false);
const loadingDetail = ref(false);
const loadingTestCases = ref(false);
const sending = ref(false);
const savingTestCase = ref(false);
const saveDialogVisible = ref(false);

const requestEditors = reactive<RequestEditorState>({
  headers: "",
  params: "",
  body: "",
});

const testCaseForm = reactive<TestCaseFormState>({
  name: "",
  description: "",
  expectedStatus: "",
  expectedKeywords: "",
  remark: "",
});

const debugResult = ref<InterfaceDebugResponse | null>(null);

const responseText = computed(() => {
  if (!debugResult.value) {
    return "Send a request to see the response.";
  }

  const data = debugResult.value.data;
  if (data == null) {
    return "";
  }

  return typeof data === "string" ? data : JSON.stringify(data, null, 2);
});

function stringifyJson(value: JsonObject | null | undefined) {
  if (!value) {
    return "";
  }

  return JSON.stringify(value, null, 2);
}

function parseJsonObject(text: string, label: string) {
  const trimmed = text.trim();

  if (!trimmed) {
    return null;
  }

  let parsed: unknown;

  try {
    parsed = JSON.parse(trimmed);
  } catch {
    throw new Error(`${label} must be valid JSON`);
  }

  if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") {
    throw new Error(`${label} must be a JSON object`);
  }

  return parsed as JsonObject;
}

function fillEditors(data: InterfaceItem) {
  requestEditors.headers = stringifyJson(data.headers);
  requestEditors.params = stringifyJson(data.params);
  requestEditors.body = stringifyJson(data.body);
}

function fillEditorsFromTestCase(testCase: InterfaceTestCaseItem) {
  requestEditors.headers = stringifyJson(testCase.request_headers);
  requestEditors.params = stringifyJson(testCase.request_params);
  requestEditors.body = stringifyJson(testCase.request_body);
}

function resetTestCaseForm() {
  testCaseForm.name = currentInterface.value
    ? `${currentInterface.value.name} Debug Case`
    : "";
  testCaseForm.description = "";
  testCaseForm.expectedStatus =
    debugResult.value?.status_code?.toString() || "";
  testCaseForm.expectedKeywords = "";
  testCaseForm.remark = "";
}

async function loadInterfaceList() {
  loadingInterfaces.value = true;

  try {
    const data = await getInterfaceListApi({
      page: 1,
      page_size: 100,
    });

    interfaces.value = data.items;

    const queryId = Number(route.query.id);
    const matchedId =
      Number.isFinite(queryId) && data.items.some((item) => item.id === queryId)
        ? queryId
        : null;
    const nextId = matchedId ?? data.items[0]?.id ?? null;

    if (nextId) {
      await handleInterfaceChange(nextId);
    } else {
      selectedInterfaceId.value = null;
      currentInterface.value = null;
    }
  } catch (error: any) {
    ElMessage.error(
      error?.response?.data?.detail || "Failed to load interfaces",
    );
  } finally {
    loadingInterfaces.value = false;
  }
}

async function loadTestCases(interfaceId: number) {
  loadingTestCases.value = true;

  try {
    const data = await getInterfaceTestCasesApi(interfaceId);
    testCases.value = data;

    if (!data.some((item) => item.id === selectedTestCaseId.value)) {
      selectedTestCaseId.value = null;
    }
  } catch (error: any) {
    testCases.value = [];
    selectedTestCaseId.value = null;
    ElMessage.error(
      error?.response?.data?.detail || "Failed to load test cases",
    );
  } finally {
    loadingTestCases.value = false;
  }
}

async function handleInterfaceChange(interfaceId: number) {
  if (!interfaceId) {
    return;
  }

  selectedInterfaceId.value = interfaceId;
  loadingDetail.value = true;
  debugResult.value = null;

  try {
    const data = await getInterfaceDetailApi(interfaceId);
    currentInterface.value = data;
    selectedTestCaseId.value = null;
    fillEditors(data);
    await loadTestCases(interfaceId);

    await router.replace({
      path: route.path,
      query: { ...route.query, id: String(interfaceId) },
    });
  } catch (error: any) {
    ElMessage.error(
      error?.response?.data?.detail || "Failed to load interface detail",
    );
  } finally {
    loadingDetail.value = false;
  }
}

async function handleInterfaceSelect(value: number | null) {
  if (!value) {
    selectedInterfaceId.value = null;
    currentInterface.value = null;
    debugResult.value = null;
    testCases.value = [];
    selectedTestCaseId.value = null;
    requestEditors.headers = "";
    requestEditors.params = "";
    requestEditors.body = "";

    await router.replace({
      path: route.path,
      query: Object.fromEntries(
        Object.entries(route.query).filter(([key]) => key !== "id"),
      ),
    });
    return;
  }

  await handleInterfaceChange(value);
}

function handleTestCaseSelect(value: number | null) {
  selectedTestCaseId.value = value;

  if (!value) {
    if (currentInterface.value) {
      fillEditors(currentInterface.value);
    }
    return;
  }

  const selected = testCases.value.find((item) => item.id === value);
  if (selected) {
    fillEditorsFromTestCase(selected);
  }
}

async function handleSend() {
  if (!selectedInterfaceId.value || !currentInterface.value) {
    ElMessage.warning("Please select an interface");
    return;
  }

  let headers: JsonObject | null;
  let params: JsonObject | null;
  let body: JsonObject | null;

  try {
    headers = parseJsonObject(requestEditors.headers, "Headers");
    params = parseJsonObject(requestEditors.params, "Params");
    body = parseJsonObject(requestEditors.body, "Body");
  } catch (error: any) {
    ElMessage.error(error.message || "Invalid JSON input");
    return;
  }

  sending.value = true;

  try {
    const requestBody = ["GET", "HEAD"].includes(
      currentInterface.value.method.toUpperCase(),
    )
      ? null
      : body;

    const data = await debugInterfaceApi(selectedInterfaceId.value, {
      headers,
      params,
      body: requestBody,
    });

    debugResult.value = data;

    ElMessage.success(
      data.success
        ? "Request sent successfully"
        : "Request finished with error",
    );
  } catch (error: any) {
    const message =
      error?.response?.data?.detail || "Failed to send debug request";
    ElMessage.error(message);
  } finally {
    sending.value = false;
  }
}

function openSaveTestCaseDialog() {
  if (!selectedInterfaceId.value || !currentInterface.value) {
    ElMessage.warning("Please select an interface first");
    return;
  }

  resetTestCaseForm();
  saveDialogVisible.value = true;
}

async function handleSaveTestCase() {
  if (!selectedInterfaceId.value) {
    return;
  }

  if (!testCaseForm.name.trim()) {
    ElMessage.warning("Please enter a test case name");
    return;
  }

  if (
    testCaseForm.expectedStatus &&
    Number.isNaN(Number(testCaseForm.expectedStatus))
  ) {
    ElMessage.warning("Expected status must be a number");
    return;
  }

  let requestHeaders: JsonObject | null;
  let requestParams: JsonObject | null;
  let requestBody: JsonObject | null;

  try {
    requestHeaders = parseJsonObject(requestEditors.headers, "Headers");
    requestParams = parseJsonObject(requestEditors.params, "Params");
    requestBody = parseJsonObject(requestEditors.body, "Body");
  } catch (error: any) {
    ElMessage.error(error.message || "Invalid JSON input");
    return;
  }

  savingTestCase.value = true;

  try {
    const created = await createInterfaceTestCaseApi(selectedInterfaceId.value, {
      name: testCaseForm.name.trim(),
      description: testCaseForm.description.trim() || null,
      request_headers: requestHeaders,
      request_params: requestParams,
      request_body: requestBody,
      expected_status: testCaseForm.expectedStatus
        ? Number(testCaseForm.expectedStatus)
        : null,
      expected_keywords: testCaseForm.expectedKeywords.trim() || null,
      remark: testCaseForm.remark.trim() || null,
    });

    await loadTestCases(selectedInterfaceId.value);
    selectedTestCaseId.value = created.id;
    fillEditorsFromTestCase(created);
    ElMessage.success("Test case saved");
    saveDialogVisible.value = false;
  } catch (error: any) {
    ElMessage.error(
      error?.response?.data?.detail || "Failed to save test case",
    );
  } finally {
    savingTestCase.value = false;
  }
}

onMounted(() => {
  loadInterfaceList();
});
</script>

<template>
  <div class="interface-debug-page">
    <el-row :gutter="16" class="page-row">
      <el-col :xl="6" :lg="7" :md="24">
        <el-card shadow="never" class="full-height">
          <template #header>
            <span>Interface Info</span>
          </template>

          <div class="card-content">
            <el-form label-position="top">
              <el-form-item label="Select Interface">
                <el-select
                  v-model="selectedInterfaceId"
                  placeholder="Select interface"
                  filterable
                  clearable
                  :loading="loadingInterfaces"
                  style="width: 100%"
                  @change="handleInterfaceSelect"
                >
                  <el-option
                    v-for="item in interfaces"
                    :key="item.id"
                    :label="`${item.name} (${item.method})`"
                    :value="item.id"
                  />
                </el-select>
              </el-form-item>
            </el-form>

            <el-empty
              v-if="!currentInterface && !loadingDetail"
              description="No interface selected"
            />

            <div v-else v-loading="loadingDetail" class="detail-wrapper">
              <el-descriptions :column="1" border size="small">
                <el-descriptions-item label="Name">
                  {{ currentInterface?.name || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="Method">
                  <el-tag size="small">
                    {{ currentInterface?.method || "-" }}
                  </el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="URL">
                  {{ currentInterface?.url || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="Category">
                  {{ currentInterface?.category || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="Auth">
                  {{ currentInterface?.auth_type || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="Status">
                  <el-tag
                    :type="
                      currentInterface?.is_enabled === 1 ? 'success' : 'info'
                    "
                    size="small"
                  >
                    {{
                      currentInterface?.is_enabled === 1
                        ? "Enabled"
                        : "Disabled"
                    }}
                  </el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="Description">
                  {{ currentInterface?.description || "-" }}
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xl="10" :lg="9" :md="24">
        <el-card shadow="never" class="full-height">
          <template #header>
            <div class="card-header">
              <span>Request Editor</span>
              <div class="card-actions">
                <el-button
                  @click="currentInterface && fillEditors(currentInterface)"
                >
                  Reset
                </el-button>
                <el-button @click="openSaveTestCaseDialog">
                  Save Test Case
                </el-button>
                <el-button
                  type="primary"
                  :loading="sending"
                  @click="handleSend"
                >
                  Send Request
                </el-button>
              </div>
            </div>
          </template>

          <div class="card-content form-scroll-area">
            <el-form label-position="top">
              <el-form-item label="Test Case">
                <el-select
                  v-model="selectedTestCaseId"
                  placeholder="Select saved test case"
                  clearable
                  filterable
                  :loading="loadingTestCases"
                  style="width: 100%"
                  @change="handleTestCaseSelect"
                >
                  <el-option
                    v-for="item in testCases"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                  />
                </el-select>
              </el-form-item>

              <el-form-item label="Headers">
                <el-input
                  v-model="requestEditors.headers"
                  type="textarea"
                  :rows="8"
                  placeholder='{"Content-Type":"application/json"}'
                />
              </el-form-item>

              <el-form-item label="Params">
                <el-input
                  v-model="requestEditors.params"
                  type="textarea"
                  :rows="8"
                  placeholder='{"page":1,"page_size":20}'
                />
              </el-form-item>

              <el-form-item label="Body">
                <el-input
                  v-model="requestEditors.body"
                  type="textarea"
                  :rows="10"
                  placeholder='{"key":"value"}'
                />
              </el-form-item>
            </el-form>
          </div>
        </el-card>
      </el-col>

      <el-col :xl="8" :lg="8" :md="24">
        <el-card shadow="never" class="full-height">
          <template #header>
            <span>Debug Result</span>
          </template>

          <div class="card-content">
            <div class="result-meta">
              <el-tag
                :type="
                  debugResult?.success
                    ? 'success'
                    : debugResult
                      ? 'danger'
                      : 'info'
                "
              >
                {{
                  debugResult
                    ? debugResult.success
                      ? "Success"
                      : "Failed"
                    : "Pending"
                }}
              </el-tag>

              <el-tag type="info">
                Status: {{ debugResult?.status_code ?? "-" }}
              </el-tag>

              <el-tag type="warning">
                Time: {{ debugResult?.duration_ms ?? "-" }} ms
              </el-tag>
            </div>

            <el-alert
              v-if="debugResult?.error_message"
              type="error"
              :title="debugResult.error_message"
              :closable="false"
              class="result-alert"
            />

            <div class="result-section">
              <div class="section-title">JSON Response</div>
              <pre class="response-body">{{ responseText }}</pre>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="saveDialogVisible" title="Save Test Case" width="560px">
      <el-form label-width="120px">
        <el-form-item label="Name">
          <el-input
            v-model="testCaseForm.name"
            placeholder="Enter test case name"
          />
        </el-form-item>

        <el-form-item label="Description">
          <el-input
            v-model="testCaseForm.description"
            type="textarea"
            :rows="2"
            placeholder="Optional description"
          />
        </el-form-item>

        <el-form-item label="Expected Status">
          <el-input
            v-model="testCaseForm.expectedStatus"
            placeholder="e.g. 200"
          />
        </el-form-item>

        <el-form-item label="Keywords">
          <el-input
            v-model="testCaseForm.expectedKeywords"
            placeholder="Optional expected keywords, comma separated"
          />
        </el-form-item>

        <el-form-item label="Remark">
          <el-input
            v-model="testCaseForm.remark"
            type="textarea"
            :rows="2"
            placeholder="Optional remark"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div>
          <el-button @click="saveDialogVisible = false">Cancel</el-button>
          <el-button
            type="primary"
            :loading="savingTestCase"
            @click="handleSaveTestCase"
          >
            Save
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.interface-debug-page {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.page-row {
  align-items: stretch;
}

.interface-debug-page :deep(.el-col) {
  display: flex;
  margin-bottom: 16px;
  min-height: 0;
}

.full-height {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 关键：让 el-card body 成为受约束的 flex 容器 */
.full-height :deep(.el-card__body) {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.card-content {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.detail-wrapper {
  flex: 1;
  min-height: 0;
  overflow: auto;
}

.form-scroll-area {
  overflow: auto;
  padding-right: 4px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.card-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.result-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.result-alert {
  margin-bottom: 16px;
}

.result-section {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 8px;
  min-height: 0;
  overflow: hidden;
}

.section-title {
  flex-shrink: 0;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.response-body {
  flex: 1;
  max-height: 640px;
  margin: 0;
  padding: 16px;
  border-radius: 8px;
  background: #111827;
  color: #e5eefc;
  font-size: 13px;
  line-height: 1.5;
  font-family: "JetBrains Mono", "Fira Code", Consolas, Monaco, monospace;
  overflow: auto;
  overscroll-behavior: contain;
  white-space: pre-wrap;
  word-break: break-word;
  box-sizing: border-box;
}

/* 可选：让 textarea 在窄屏下更稳定 */
.interface-debug-page :deep(.el-textarea__inner) {
  font-family: "JetBrains Mono", "Fira Code", Consolas, Monaco, monospace;
}

/* 小屏时避免三列内容挤压过高 */
@media (max-width: 992px) {
  .interface-debug-page :deep(.el-col) {
    margin-bottom: 12px;
  }

  .card-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .card-actions {
    width: 100%;
  }
}
</style>
