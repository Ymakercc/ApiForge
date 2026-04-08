import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";
import axios from "axios";

const TOKEN_KEY = "token";
const USER_INFO_KEY = "userInfo";

const instance: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8020",
  timeout: 25000,
});

instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

instance.interceptors.response.use(
  (response: AxiosResponse) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_INFO_KEY);

      if (window.location.pathname !== "/login") {
        const redirect = encodeURIComponent(
          window.location.pathname + window.location.search,
        );
        window.location.href = `/login?redirect=${redirect}`;
      }
    }
    return Promise.reject(error);
  },
);

export function get<T = any>(
  url: string,
  params?: object,
  config?: AxiosRequestConfig,
): Promise<T> {
  return instance.get(url, { params, ...config });
}

export function post<T = any>(
  url: string,
  data?: object,
  config?: AxiosRequestConfig,
): Promise<T> {
  return instance.post(url, data, config);
}

export function put<T = any>(
  url: string,
  data?: object,
  config?: AxiosRequestConfig,
): Promise<T> {
  return instance.put(url, data, config);
}

export function patch<T = any>(
  url: string,
  data?: object,
  config?: AxiosRequestConfig,
): Promise<T> {
  return instance.patch(url, data, config);
}

export function del<T = any>(
  url: string,
  config?: AxiosRequestConfig,
): Promise<T> {
  return instance.delete(url, config);
}

export default instance;
