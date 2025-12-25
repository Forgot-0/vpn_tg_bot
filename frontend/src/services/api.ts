import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig, AxiosResponse } from 'axios';
import { API_BASE_URL } from '../utils/config';
import type {
  AccessTokenResponse,
  User,
  Subscription,
  VPNConfig,
  LoginTelegramRequest,
  CreateSubscriptionRequest,
  RenewSubscriptionRequest,
  PriceSubscriptionResponse,
  PaginatedResult,
  ApiError,
  ApiType,
  CreateServerRequest,
} from '../types';

class ApiClient {
  private client: AxiosInstance;
  private accessToken: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true, // Для работы с cookies (refresh token)
      timeout: 15000, // 15 секунд timeout
    });

    // Interceptor для добавления токена
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        if (this.accessToken && config.headers) {
          config.headers.Authorization = `Bearer ${this.accessToken}`;
        }
        // Для Mini App: если используется относительный URL, не добавляем базовый URL повторно
        console.debug('API Request:', config.baseURL + config.url);
        return config;
      },
      (error: AxiosError) => {
        console.error('Request Error:', error.message);
        return Promise.reject(error);
      }
    );

    // Interceptor для обработки ошибок
    this.client.interceptors.response.use(
      (response: AxiosResponse) => response,
      async (error: AxiosError<ApiError>) => {
        console.error('Response Error:', error.message, error.code, error.response?.status);
        
        // Обработка сетевых ошибок в Mini App
        if (!error.response && error.code === 'ERR_NETWORK') {
          console.error('Network error - backend may be unreachable');
          // Пытаемся понять, на каком URL мы
          console.debug('Current base URL:', API_BASE_URL);
          console.debug('Current origin:', window.location.origin);
        }

        if (error.response?.status === 401 && this.accessToken) {
          // Попытка обновить токен
          try {
            await this.refreshToken();
            // Повтор запроса
            if (error.config) {
              return this.client.request(error.config);
            }
          } catch (refreshError) {
            this.setAccessToken(null);
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  setAccessToken(token: string | null) {
    this.accessToken = token;
    if (token) {
      localStorage.setItem('access_token', token);
    } else {
      localStorage.removeItem('access_token');
    }
  }

  getAccessToken(): string | null {
    if (!this.accessToken) {
      this.accessToken = localStorage.getItem('access_token');
    }
    return this.accessToken;
  }

  // Auth
  async loginByTelegram(initData: string): Promise<AccessTokenResponse> {
    const response = await this.client.post<AccessTokenResponse>(
      '/auth/login_by_tg',
      { init_data: initData } as LoginTelegramRequest
    );
    this.setAccessToken(response.data.access_token);
    return response.data;
  }

  async refreshToken(): Promise<AccessTokenResponse> {
    const response = await this.client.post<AccessTokenResponse>('/auth/refresh');
    this.setAccessToken(response.data.access_token);
    return response.data;
  }

  // Users
  async getMe(): Promise<User> {
    const response = await this.client.get<User>('/users/me');
    return response.data;
  }

  async getUserSubscriptions(userId: string): Promise<Subscription[]> {
    const response = await this.client.get<Subscription[]>(`/users/${userId}/subscriptions`);
    return response.data;
  }

  // Subscriptions
  async getSubscriptions(page = 1, pageSize = 10): Promise<PaginatedResult<Subscription>> {
    const response = await this.client.get<PaginatedResult<Subscription>>('/subscrtiption/', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  }

  async getSubscription(subscriptionId: string): Promise<Subscription> {
    const response = await this.client.get<Subscription>(`/subscrtiption/${subscriptionId}`);
    return response.data;
  }

  async getSubscriptionConfig(subscriptionId: string): Promise<VPNConfig> {
    const response = await this.client.get<VPNConfig>(`/subscrtiption/${subscriptionId}/config`);
    return response.data;
  }

  async createSubscription(data: CreateSubscriptionRequest): Promise<string> {
    try {
      const response = await this.client.post('/subscrtiption/', data, {
        maxRedirects: 0,
        validateStatus: (status: number) => status >= 200 && status < 400,
      });
      // Возвращаем URL для редиректа
      if (response.status === 307 || response.status === 200) {
        const location = response.headers.location;
        if (location) {
          return location;
        }
        // Если location в заголовках нет, проверяем data
        if (typeof response.data === 'string' && response.data.startsWith('http')) {
          return response.data;
        }
      }
      throw new Error('Failed to get payment URL');
    } catch (error: any) {
      if (error.response?.status === 307 || error.response?.status === 200) {
        const location = error.response?.headers?.location;
        if (location) {
          return location;
        }
      }
      throw error;
    }
  }

  async renewSubscription(
    subscriptionId: string,
    data: RenewSubscriptionRequest
  ): Promise<string> {
    try {
        const response = await this.client.post(
        `/subscrtiption/${subscriptionId}/renew`,
        data,
        {
          maxRedirects: 0,
          validateStatus: (status: number) => status >= 200 && status < 400,
        }
      );
      if (response.status === 307 || response.status === 200) {
        const location = response.headers.location;
        if (location) {
          return location;
        }
        if (typeof response.data === 'string' && response.data.startsWith('http')) {
          return response.data;
        }
      }
      throw new Error('Failed to get payment URL');
    } catch (error: any) {
      if (error.response?.status === 307 || error.response?.status === 200) {
        const location = error.response?.headers?.location;
        if (location) {
          return location;
        }
      }
      throw error;
    }
  }

  async getPrice(data: CreateSubscriptionRequest): Promise<number> {
    const response = await this.client.post<PriceSubscriptionResponse>(
      '/subscrtiption/get_price',
      data
    );
    return response.data.price;
  }

  // Servers
  async createServer(apiType: ApiType, data: CreateServerRequest): Promise<void> {
    await this.client.post(`/servers/${apiType}`, data);
  }
}

export const apiClient = new ApiClient();

