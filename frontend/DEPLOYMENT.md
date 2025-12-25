# Развертывание Frontend

## Локальная разработка

1. Установите зависимости:
```bash
cd frontend
npm install
```

2. Создайте файл `.env`:
```bash
cp .env.example .env
# Отредактируйте .env и укажите VITE_API_BASE_URL
```

3. Запустите dev-сервер:
```bash
npm run dev
```

Приложение будет доступно на `http://localhost:3000`

## Production сборка

1. Соберите проект:
```bash
npm run build
```

2. Файлы будут в папке `dist/`

3. Настройте Nginx для раздачи статических файлов:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    root /path/to/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Кеширование статических ресурсов
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## Интеграция с Telegram Bot

1. Настройте Mini App в вашем Telegram боте через [@BotFather](https://t.me/BotFather):
   - Отправьте команду `/newapp`
   - Выберите вашего бота
   - Укажите название и описание приложения
   - Укажите URL: `https://yourdomain.com`
   - Загрузите иконку (опционально)

2. Убедитесь, что CORS настроен на бэкенде для вашего домена

3. Проверьте, что бэкенд доступен по указанному в `.env` адресу

## Переменные окружения

- `VITE_API_BASE_URL` - базовый URL API бэкенда (обязательно)

## Docker (опционально)

Можно добавить в `docker-compose.yml`:

```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
  ports:
    - "3000:80"
  environment:
    - VITE_API_BASE_URL=https://yourdomain.com/api/v1
```

И создать `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

