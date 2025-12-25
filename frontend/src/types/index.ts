export interface User {
  id: string;
  telegram_id: number;
  username?: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  role: string;
  created_at: string;
  updated_at: string;
}

export interface Subscription {
  id: string;
  user_id: string;
  server_id: string;
  duration_days: number;
  device_count: number;
  protocol_types: string[];
  status: string;
  expires_at: string;
  created_at: string;
  updated_at: string;
}

export interface VPNConfig {
  protocol: string;
  config: string;
  qr_code?: string;
}

export interface AccessTokenResponse {
  access_token: string;
}

export interface LoginTelegramRequest {
  init_data: string;
}

export interface CreateSubscriptionRequest {
  duration_days: number;
  device_count: number;
  protocol_types: string[];
}

export interface RenewSubscriptionRequest {
  duration_days: number;
}

export interface PriceSubscriptionResponse {
  price: number;
}

export interface PaginatedResult<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    detail?: string;
  };
  status: number;
  request_id: string;
  timestamp: number;
}

export type ApiType = '3X-UI';

export interface CreateServerRequest {
  limit: number;
  region_code: string;
  ip: string;
  panel_port: number;
  panel_path: string;
  domain?: string | null;
  username: string;
  password: string;
  twoFactorCode?: string | null;
}

