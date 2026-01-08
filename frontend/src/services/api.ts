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
  Server,
  ServerDetail,
  Payment,
  PaymentUrlResponse,
  PriceConfig,
  AddProtocolPriceRequest,
  AddRegionPriceRequest,
  UpdatePriceRequest,
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
      paramsSerializer: {
        indexes: null, // Сериализация массивов как повторяющиеся параметры (protocol_types=vless&protocol_types=vmess)
      },
    });

    // Interceptor для добавления токена
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        if (this.accessToken && config.headers) {
          config.headers.Authorization = `Bearer ${this.accessToken}`;
        }
        // Для Mini App: если используется относительный URL, не добавляем базовый URL повторно
        if (config.baseURL && config.url) {
          console.debug('API Request:', config.baseURL + config.url);
        }
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

  async getUserSubscriptions(userId?: string): Promise<Subscription[]> {
    // Если userId не передан, получаем текущего пользователя и используем его id
    const targetUserId = userId || (await this.getMe()).id;
    const response = await this.client.get<Subscription[]>(`/users/${targetUserId}/subscriptions`);
    return response.data;
  }

  // Subscriptions
  async getSubscriptions(page = 1, pageSize = 10): Promise<PaginatedResult<Subscription>> {
    const response = await this.client.get<PaginatedResult<Subscription>>('/subscription/', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  }

  async getSubscription(subscriptionId: string): Promise<Subscription> {
    const response = await this.client.get<Subscription>(`/subscription/${subscriptionId}`);
    return response.data;
  }

  async getSubscriptionConfig(subscriptionId: string): Promise<VPNConfig[]> {
    const response = await this.client.get<VPNConfig[]>(`/subscription/${subscriptionId}/config`);
    return response.data;
  }

  async createSubscription(data: CreateSubscriptionRequest): Promise<string> {
    const response = await this.client.post<PaymentUrlResponse>('/subscription/', data);
    return response.data.url;
  }

  async renewSubscription(
    subscriptionId: string,
    data: RenewSubscriptionRequest
  ): Promise<string> {
    const response = await this.client.post<PaymentUrlResponse>(
      `/subscription/${subscriptionId}/renew`,
      data
    );
    return response.data.url;
  }

  async getPrice(data: CreateSubscriptionRequest): Promise<number> {
    const response = await this.client.post<PriceSubscriptionResponse>(
      '/subscription/get_price',
      data
    );
    return response.data.price;
  }

  // Servers (Admin only)
  async getServers(
    page = 1,
    pageSize = 10,
    filters?: {
      region_code?: string;
      api_type?: string;
      min_free_slots?: number;
      max_free_slots?: number;
      protocol_types?: string[];
      has_domain?: boolean;
    },
    sort?: string
  ): Promise<PaginatedResult<Server>> {
    const params: any = { page, page_size: pageSize };
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params[key] = value;
        }
      });
    }
    if (sort) {
      params.sort = sort;
    }
    const response = await this.client.get<PaginatedResult<Server>>('/servers/', { params });
    return response.data;
  }

  async getServer(serverId: string): Promise<ServerDetail> {
    const response = await this.client.get<ServerDetail>(`/servers/${serverId}`);
    return response.data;
  }

  async createServer(apiType: ApiType, data: CreateServerRequest): Promise<void> {
    await this.client.post(`/servers/${apiType}`, data);
  }

  async deleteServer(serverId: string): Promise<void> {
    await this.client.delete(`/servers/${serverId}`);
  }

  async reloadServerConfig(serverId: string): Promise<void> {
    await this.client.post(`/servers/${serverId}/reload_config`);
  }

  // Users (Admin only)
  async getUser(userId: string): Promise<User> {
    const response = await this.client.get<User>(`/users/${userId}`);
    return response.data;
  }

  async getUsers(
    page = 1,
    pageSize = 10,
    filters?: {
      telegram_id?: number;
      role?: string;
      is_premium?: boolean;
      username?: string;
      fullname?: string;
      phone?: string;
      referred_by_id?: string;
      created_after?: string; // ISO datetime string
      created_before?: string; // ISO datetime string
      has_subscriptions?: boolean;
      min_referrals_count?: number;
    },
    sort?: string
  ): Promise<PaginatedResult<User>> {
    const params: any = { page, page_size: pageSize };
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params[key] = value;
        }
      });
    }
    if (sort) {
      params.sort = sort;
    }
    const response = await this.client.get<PaginatedResult<User>>('/users/', { params });
    return response.data;
  }

  // Subscriptions (Admin only) with filters
  async getAllSubscriptions(
    page = 1,
    pageSize = 10,
    filters?: {
      user_id?: string;
      server_id?: string;
      region_code?: string;
      status?: string;
      protocol_types?: string[];
      min_duration?: number;
      max_duration?: number;
      start_date_after?: string; // ISO datetime string
      start_date_before?: string; // ISO datetime string
      min_device_count?: number;
      max_device_count?: number;
    },
    sort?: string
  ): Promise<PaginatedResult<Subscription>> {
    const params: any = { page, page_size: pageSize };
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params[key] = value;
        }
      });
    }
    if (sort) {
      params.sort = sort;
    }
    const response = await this.client.get<PaginatedResult<Subscription>>('/subscription/', {
      params,
    });
    return response.data;
  }

  // Payments (Admin only)
  async getPayment(paymentId: string): Promise<Payment> {
    const response = await this.client.get<Payment>(`/payments/${paymentId}`);
    return response.data;
  }

  async getPayments(
    page = 1,
    pageSize = 10,
    filters?: {
      user_id?: string;
      subscription_id?: string;
      status?: string;
      min_price?: number;
      max_price?: number;
      payment_date_after?: string; // ISO datetime string
      payment_date_before?: string; // ISO datetime string
      created_after?: string; // ISO datetime string
      created_before?: string; // ISO datetime string
      has_payment_id?: boolean;
    },
    sort?: string
  ): Promise<PaginatedResult<Payment>> {
    const params: any = { page, page_size: pageSize };
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params[key] = value;
        }
      });
    }
    if (sort) {
      params.sort = sort;
    }
    const response = await this.client.get<PaginatedResult<Payment>>('/payments/', { params });
    return response.data;
  }

  // Change user role (Admin only)
  async changeUserRole(userId: string, role: string): Promise<void> {
    await this.client.post(`/users/${userId}/change_role/${role}`);
  }

  // Price management (Admin only)
  async getPriceConfig(): Promise<PriceConfig> {
    const response = await this.client.get<PriceConfig>('/price/');
    return response.data;
  }

  async addProtocolPrice(data: AddProtocolPriceRequest): Promise<void> {
    await this.client.post('/price/add_protocol', data);
  }

  async addRegionPrice(data: AddRegionPriceRequest): Promise<void> {
    await this.client.post('/price/add_region', data);
  }

  async updatePrice(data: UpdatePriceRequest): Promise<void> {
    await this.client.patch('/price/', data);
  }
}

export const apiClient = new ApiClient();

