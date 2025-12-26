// Функция для получения API base URL
const getApiBaseUrl = (): string => {
  // Если установлена переменная окружения - используем её
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  return ""
};

export const API_BASE_URL = getApiBaseUrl();

// Telegram WebApp
export const TELEGRAM_WEBAPP = window.Telegram?.WebApp;

