import { del, get, patch, post, put } from '@/utils/request'

export interface JsonObject {
  [key: string]: any
}

export interface InterfaceItem {
  id: number
  name: string
  description: string | null
  method: string
  url: string
  headers: JsonObject | null
  params: JsonObject | null
  body: JsonObject | null
  auth_type: string
  auth_config: JsonObject | null
  category: string | null
  is_enabled: number
  created_by: number | null
  created_at: string
  updated_at: string
}

export interface InterfaceListParams {
  page?: number
  page_size?: number
  keyword?: string
}

export interface InterfaceListResponse {
  total: number
  page: number
  page_size: number
  items: InterfaceItem[]
}

export interface InterfaceFormData {
  name: string
  description?: string | null
  method: string
  url: string
  headers?: JsonObject | null
  params?: JsonObject | null
  body?: JsonObject | null
  category?: string | null
  auth_type?: string
  auth_config?: JsonObject | null
  is_enabled?: number
}

export interface InterfaceDebugPayload {
  headers?: JsonObject | null
  params?: JsonObject | null
  body?: JsonObject | null
}

export interface InterfaceDebugResponse {
  success: boolean
  status_code: number | null
  duration_ms: number
  data: any
  error_message: string | null
}

export interface InterfaceTestCasePayload {
  name: string
  description?: string | null
  request_headers?: JsonObject | null
  request_params?: JsonObject | null
  request_body?: JsonObject | null
  expected_status?: number | null
  expected_keywords?: string | null
  remark?: string | null
}

export interface InterfaceTestCaseItem {
  id: number
  interface_id: number
  name: string
  description: string | null
  request_headers: JsonObject | null
  request_params: JsonObject | null
  request_body: JsonObject | null
  expected_status: number | null
  expected_keywords: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

export function getInterfaceListApi(params: InterfaceListParams) {
  return get<InterfaceListResponse>('/api/v1/interfaces', params)
}

export function createInterfaceApi(data: InterfaceFormData) {
  return post<InterfaceItem>('/api/v1/interfaces', data)
}

export function getInterfaceDetailApi(interfaceId: number) {
  return get<InterfaceItem>(`/api/v1/interfaces/${interfaceId}`)
}

export function updateInterfaceApi(interfaceId: number, data: Partial<InterfaceFormData>) {
  return put<InterfaceItem>(`/api/v1/interfaces/${interfaceId}`, data)
}

export function deleteInterfaceApi(interfaceId: number) {
  return del<void>(`/api/v1/interfaces/${interfaceId}`)
}

export function updateInterfaceStatusApi(interfaceId: number, isEnabled: number) {
  return patch<InterfaceItem>(`/api/v1/interfaces/${interfaceId}/status`, {
    is_enabled: isEnabled,
  })
}

export function debugInterfaceApi(interfaceId: number, data: InterfaceDebugPayload) {
  return post<InterfaceDebugResponse>(`/api/v1/interfaces/${interfaceId}/debug`, data)
}

export function getInterfaceTestCasesApi(interfaceId: number) {
  return get<InterfaceTestCaseItem[]>(`/api/v1/interfaces/${interfaceId}/test-cases`)
}

export function createInterfaceTestCaseApi(interfaceId: number, data: InterfaceTestCasePayload) {
  return post<InterfaceTestCaseItem>(`/api/v1/interfaces/${interfaceId}/test-cases`, data)
}
