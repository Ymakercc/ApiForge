import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getMeApi, loginApi, type LoginParams, type UserInfo } from '@/api/auth'

const TOKEN_KEY = 'token'
const USER_INFO_KEY = 'userInfo'

function getStoredUserInfo() {
  const raw = localStorage.getItem(USER_INFO_KEY)

  if (!raw) {
    return null
  }

  try {
    return JSON.parse(raw) as UserInfo
  } catch {
    localStorage.removeItem(USER_INFO_KEY)
    return null
  }
}

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(localStorage.getItem(TOKEN_KEY) || '')
  const userInfo = ref<UserInfo | null>(getStoredUserInfo())

  function setToken(val: string) {
    token.value = val
    localStorage.setItem(TOKEN_KEY, val)
  }

  function setUserInfo(val: UserInfo | null) {
    userInfo.value = val

    if (val) {
      localStorage.setItem(USER_INFO_KEY, JSON.stringify(val))
      return
    }

    localStorage.removeItem(USER_INFO_KEY)
  }

  async function fetchUserInfo() {
    try {
      const data = await getMeApi()
      setUserInfo(data)
      return data
    } catch (error) {
      logout()
      throw error
    }
  }

  async function login(payload: LoginParams) {
    const data = await loginApi(payload)
    setToken(data.access_token)
    await fetchUserInfo()
    return data
  }

  function logout() {
    token.value = ''
    setUserInfo(null)
    localStorage.removeItem(TOKEN_KEY)
  }

  const isLoggedIn = () => !!token.value

  return { token, userInfo, setToken, setUserInfo, fetchUserInfo, login, logout, isLoggedIn }
})
