
# Telegram Bot with YooKassa Payment Integration

Этот проект реализует Telegram-бота, который интегрируется с платежной системой YooKassa с помощью веб-хуков. Архитектура следует шаблонам Domain-Driven Design (DDD) и Command Query Responsibility Segregation (CQRS), обеспечивая чистую и поддерживаемую кодовую базу.

Пощупать бота можна [@forgot_vpn_bot](https://t.me/forgot_vpn_bot)

## Tech Stack

- **Bot Framework**: [Aiogram](https://aiogram.dev/)
- **Database**: [MongoDB](https://www.mongodb.com/)
- **Web App**: [aiohttp](https://docs.aiohttp.org/en/stable/)
- **Web Server**: [Nginx](https://www.nginx.com/)
- **Containerization**: [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- **SSL Certificates**: [Certbot](https://certbot.eff.org/)
- **ORM**: [Motor](https://motor.readthedocs.io/en/stable/)

## Деплой бота с использованием Nginx

Проект можно задеплоить, используя Docker Compose напрямую. Важно: сначала необходимо подписать SSL-сертификаты, а затем запускать Nginx c портом 443.

**Шаг 1. Подготовка и подпись сертификатов:**

1. Отредактируйте файл `nginx/nginx.conf`(убрав 443 порт), заменив переменную `$DOMAIN` на ваш актуальный домен. (подробнее можно узнать здесь [ссылка](https://github.com/ssharkexe/telegram-nginx-docker-webhook/blob/main/README.md))
2. Подпишите сертификаты с помощью контейнера certbot. Выполните:
   ```bash
   docker-compose -f docker_compose/webserver.yaml run --rm certbot certonly --webroot --webroot-path=/var/www/certbot -d ваш_домен
   ```
   Убедитесь, что сертификаты успешно получены и сохранены в каталоге `../nginx/ssl`.

**Шаг 2. Запуск сервисов:**

После успешного получения сертификатов поднимите контейнеры. Рекомендуется запускать их поэтапно:

1. Сначала запустите контейнер с бд:
   ```bash
   docker-compose -f docker_compose/storage.yaml up -d
   ```
2. Потом запустите контейнер с приложением:
    ```bash
   docker-compose -f docker_compose/app.yaml up -d
   ```
3. Затем запустите контейнеры для веб-сервера (Nginx) и службы обновления сертификатов:
   ```bash
   docker-compose -f docker_compose/webserver.yaml up -d
   ```

**Выбор вариантов запуска:**

- Если требуется запустить только приложение, используйте `docker_compose/app.yaml`.
- Для запуска Nginx и автоматического обновления сертификатов используйте `docker_compose/webserver.yaml`.


## Мониторинг и логирование

Проект поставляется также с настройками мониторинга и логирования, позволяющими отслеживать работу сервисов и собирать логи.

В мониторинговую инфраструктуру входят:
- **Grafana** – для визуализации метрик. Доступна на порту **3000**.
- **Loki** – для агрегации и хранения логов. Доступен на порту **3100**.
- **Vector** – для сбора и пересылки логов с контейнеров.

Для развертывания мониторинга выполните:
```bash
docker-compose -f docker_compose/monitoring.yaml up -d
```
Это поднимет все необходимые сервисы из файла [docker_compose/monitoring.yaml](docker_compose/monitoring.yaml).
