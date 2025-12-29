export interface User {
  id: string;
  telegram_id: number | null;
  username?: string | null;
  fullname?: string | null;
  phone?: string | null;
  is_premium: boolean;
  role: string;
  referred_by?: string | null;
  referrals_count: number;
  created_at: string;
  subscriptions?: Subscription[];
}

export interface Subscription {
  id: string;
  duration: number;
  start_date: string;
  device_count: number;
  user_id: string;
  server_id: string;
  flag: string;
  name: string;
  code: string;
  protocol_types: string[];
  status: string;
  expires_at?: string;
  created_at?: string;
  updated_at?: string;
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
  total_pages: number;
  has_next: boolean;
  has_previous: boolean;
  next_page: number | null;
  previous_page: number | null;
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

export interface Server {
  id: string;
  limit: number;
  region_flag: string;
  region_code: string;
  region_name: string;
  free: number;
  api_type: string;
  ip: string;
  panel_port: number;
  panel_path: string;
  domain?: string | null;
  protocol_configs: string[];
}

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

export interface Payment {
  id: string;
  subscription: Subscription;
  user_id: string;
  total_price: number;
  status: string;
  payment_id?: string | null;
  payment_date?: string | null;
  created_at: string;
}

export interface PaymentUrlResponse {
  url: string;
}

