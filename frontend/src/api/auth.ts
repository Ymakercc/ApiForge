import { get, post } from '@/utils/request'

export interface LoginParams {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface UserInfo {
  id: number
  username: string
  email: string | null
  role: string
  is_active: number
}

export function loginApi(data: LoginParams) {
  return post<LoginResponse>('/api/v1/auth/login', data)
}

export function getMeApi() {
  return get<UserInfo>('/api/v1/auth/me')
}
