import { del, get, patch, post, put } from '@/utils/request'

export interface InterfaceItem {
  id: number
  name: string
  description: string | null
  method: string
  url: string
  headers: Record<string, any> | null
  params: Record<string, any> | null
  body: Record<string, any> | null
  auth_type: string
  auth_config: Record<string, any> | null
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
  category?: string | null
  auth_type?: string
  is_enabled?: number
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
