
# Telegram Bot with YooKassa Payment Integration

This project implements a Telegram bot that integrates with the YooKassa payment system using webhooks. The architecture follows Domain-Driven Design (DDD) and Command Query Responsibility Segregation (CQRS) patterns, ensuring a clean and maintainable codebase.
Пощупать бота можна [@forgot_vpn_bot](https://t.me/forgot_vpn_bot)
## Tech Stack

- **Bot Framework**: [Aiogram](https://aiogram.dev/)
- **Database**: [MongoDB](https://www.mongodb.com/)
- **Web App**: [aiohttp](https://docs.aiohttp.org/en/stable/)
- **Web Server**: [Nginx](https://www.nginx.com/)
- **Containerization**: [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- **SSL Certificates**: [Certbot](https://certbot.eff.org/)
- **ORM**: [Motor](https://motor.readthedocs.io/en/stable/)


### Environment Variables

Create a `.env` file in the root directory with the following variables:
```bash
BOT_TOKEN=
OWNER=
DOMAIN=
USERNAME_BOT=
TELEGRAM_WEBHOOK_HOST=https://${DOMAIN}
TELEGRAM_WEBHOOK_PATH='/webhook'
TELEGRAM_WEBHOOK_URL=${TELEGRAM_WEBHOOK_HOST}${TELEGRAM_WEBHOOK_PATH}

PAYMENT_SECRET=
PAYMENT_ID=

WEBAPP_WEBHOOK_PORT=8080
WEBAPP_WEBHOOK_HOST='0.0.0.0'

PYTHONPATH=app

DATABASE_USERNAME=
DATABASE_PASSWORD=
DATABASE_PORT=27017
DATABASE_URL=mongodb://${DATABASE_USERNAME}:${DATABASE_PASSWORD}@mongo:27017/

BASICAUTH_USERNAME=
BASICAUTH_PASSWORD=

BROKER_URL=""

VPN_USERNAME=
VPN_PASSWORD=
VPN_SECRET=
```
