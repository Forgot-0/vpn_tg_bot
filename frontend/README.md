# VPN Telegram Bot - Frontend

React TypeScript приложение для Telegram Mini App, предоставляющее интерфейс для управления VPN подписками.

## Технологии

- **React 18** - UI библиотека
- **TypeScript** - типизация
- **Vite** - сборщик и dev-сервер
- **React Router** - маршрутизация
- **Axios** - HTTP клиент
- **Tailwind CSS** - стилизация
- **@twa-dev/sdk** - интеграция с Telegram WebApp API

## Установка

```bash
cd frontend
npm install
```

## Разработка

```bash
npm run dev
```

Приложение будет доступно на `http://localhost:3000`

## Сборка

```bash
npm run build
```

Собранные файлы будут в папке `dist/`

## Настройка

Создайте файл `.env` в корне проекта `frontend/`:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Для production используйте ваш домен:

```env
VITE_API_BASE_URL=https://yourdomain.com/api/v1
```

## Структура проекта

```
frontend/
├── src/
│   ├── components/      # Переиспользуемые компоненты
│   ├── contexts/        # React контексты (Auth)
│   ├── pages/           # Страницы приложения
│   ├── services/        # API клиент
│   ├── types/           # TypeScript типы
│   ├── utils/           # Утилиты
│   ├── App.tsx          # Главный компонент
│   └── main.tsx         # Точка входа
├── public/              # Статические файлы
├── index.html           # HTML шаблон
└── package.json         # Зависимости
```

## Функциональность

### Авторизация
- Вход через Telegram WebApp initData
- Автоматическое обновление токенов
- Сохранение токена в localStorage

### Подписки
- Просмотр списка подписок
- Создание новой подписки с выбором параметров
- Просмотр деталей подписки
- Получение VPN конфигурации
- Продление подписки

### Профиль
- Просмотр информации о пользователе
- Выход из аккаунта

## Интеграция с Telegram

Приложение использует Telegram WebApp API для:
- Автоматической авторизации через `initData`
- Адаптации под тему Telegram (светлая/темная)
- Использования нативных алертов и подтверждений
- Закрытия приложения

## API Endpoints

Приложение взаимодействует с следующими endpoints:

- `POST /api/v1/auth/login_by_tg` - вход через Telegram
- `POST /api/v1/auth/refresh` - обновление токена
- `GET /api/v1/users/me` - получение текущего пользователя
- `GET /api/v1/users/{user_id}/subscriptions` - подписки пользователя
- `GET /api/v1/subscrtiption/` - список подписок
- `GET /api/v1/subscrtiption/{id}` - детали подписки
- `GET /api/v1/subscrtiption/{id}/config` - конфигурация VPN
- `POST /api/v1/subscrtiption/` - создание подписки
- `POST /api/v1/subscrtiption/{id}/renew` - продление подписки
- `POST /api/v1/subscrtiption/get_price` - расчет цены

## Развертывание

1. Соберите проект: `npm run build`
2. Настройте веб-сервер (Nginx) для раздачи статических файлов из `dist/`
3. Убедитесь, что CORS настроен на бэкенде для вашего домена
4. Настройте Telegram Bot для использования вашего URL как Mini App

## Примечания

- Приложение автоматически определяет тему Telegram (светлая/темная)
- Токены сохраняются в localStorage для автоматической авторизации
- При ошибке 401 автоматически пытается обновить токен
- Все запросы идут с credentials для работы с cookies (refresh token)

