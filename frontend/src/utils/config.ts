// Функция для получения API base URL
const getApiBaseUrl = (): string => {
//   Если установлена переменная окружения - используем её
//   if (import.meta.env.VITE_API_BASE_URL) {
//     return import.meta.env.VITE_API_BASE_URL;
//   }

//   // Если запущено в Telegram Mini App - используем относительный URL
//   // Предполагаем, что backend на том же домене
//   if (window.Telegram?.WebApp?.initData) {
//     // В Mini App используем относительный URL (пройдёт через same-origin)
//     return '/api/v1';
//   }

//   // Для локальной разработки
//   if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
//     return `http://localhost:8080/api/v1`;
//   }

//   // Для production (если фронтенд и бэкенд на разных поддоменах)
//   const host = window.location.hostname;
//   if (host.includes('.')) {
//     const domain = host.split('.').slice(1).join('.');
//     return `https://api.${domain}/api/v1`;
//   }

  // Fallback
  return 'https://6fq0p29m-8080.euw.devtunnels.ms/api/v1';
};

export const API_BASE_URL = getApiBaseUrl();

// Telegram WebApp
export const TELEGRAM_WEBAPP = window.Telegram?.WebApp;

