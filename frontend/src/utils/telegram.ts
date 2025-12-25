import { TELEGRAM_WEBAPP } from './config';

export const initTelegramWebApp = () => {
  if (TELEGRAM_WEBAPP) {
    TELEGRAM_WEBAPP.ready();
    TELEGRAM_WEBAPP.expand();
    
    // Настройка цветовой схемы
    if (TELEGRAM_WEBAPP.colorScheme === 'dark') {
      document.documentElement.classList.add('dark');
    }
    
    return TELEGRAM_WEBAPP;
  }
  return null;
};

export const getTelegramInitData = (): string | null => {
  if (TELEGRAM_WEBAPP?.initData) {
    return TELEGRAM_WEBAPP.initData;
  }
  return null;
};

export const showTelegramAlert = (message: string) => {
  if (TELEGRAM_WEBAPP) {
    TELEGRAM_WEBAPP.showAlert(message);
  } else {
    alert(message);
  }
};

export const showTelegramConfirm = (message: string): Promise<boolean> => {
  return new Promise((resolve) => {
    if (TELEGRAM_WEBAPP) {
      TELEGRAM_WEBAPP.showConfirm(message, (confirmed) => {
        resolve(confirmed);
      });
    } else {
      resolve(confirm(message));
    }
  });
};

export const closeTelegramWebApp = () => {
  if (TELEGRAM_WEBAPP) {
    TELEGRAM_WEBAPP.close();
  }
};

