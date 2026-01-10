#!/usr/bin/env bash

set -euo pipefail
ENV_FILE=".env"


if [ -f .env ]; then
    echo "Файл .env уже существует. Создать резервную копию? (y/n)"
    read -r backup
    if [ "$backup" = "y" ]; then
        cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
        echo "Резервная копия создана"
    fi
fi

cp .env.example .env


generate_secret() {
  openssl rand -base64 32
}

generate_password() {
  tr -dc 'A-Za-z0-9' </dev/urandom | head -c 20
}


echo ""
echo "Заполните следующие обязательные параметры:"
echo ""


read -p "Введите ваш домен (например, example.com): " domain
sed -i "s/DOMAIN=/DOMAIN=${domain}/" .env

read -p "Введите BOT_TOKEN: " bot_token
sed -i "s/BOT_TOKEN=/BOT_TOKEN=${bot_token}/" .env

read -p "Введите BOT_OWNER_ID: " bot_owner_id
sed -i "s/BOT_OWNER_ID=/BOT_OWNER_ID=${bot_owner_id}/" .env

read -p "Введите BOT_USERNAME: " bot_username
sed -i "s/BOT_USERNAME=/BOT_USERNAME=${bot_username}/" .env


echo ""
echo "Генерация секретов..."

sed -i "s|^SECRET=.*|SECRET=$(generate_secret)|" .env
sed -i "s|^WEBHOOK_SECRET=.*|WEBHOOK_SECRET=$(generate_secret)|" .env

echo "Секреты сгенерированы автоматически"

echo ""
read -p "Введите PAYMENT_SECRET (YooKassa): " payment_secret
sed -i "s/PAYMENT_SECRET=/PAYMENT_SECRET=${payment_secret}/" .env

read -p "Введите PAYMENT_ID (YooKassa): " payment_id
sed -i "s/PAYMENT_ID=/PAYMENT_ID=${payment_id}/" .env


echo ""
read -p "Введите VPN_HELP_ACCOUNT (аккаунт для помощи): " vpn_help
sed -i "s/VPN_HELP_ACCOUNT=\"\"/VPN_HELP_ACCOUNT=\"${vpn_help}\"/" .env


# Database credentials
echo ""
read -p "Изменить DATABASE_USERNAME? (текущий: admin) [y/n]: " change_db_user
if [ "$change_db_user" = "y" ]; then
    read -p "Введите DATABASE_USERNAME: " db_username
    sed -i "s/DATABASE_USERNAME=admin/DATABASE_USERNAME=${db_username}/" .env
fi

dat=$(generate_password)

echo ""
read -p "Хотите установить свой DATABASE_PASSWORD? [y/n]: " change_db_pass
if [ "$change_db_pass" = "y" ]; then
    read -p "Введите DATABASE_PASSWORD: " db_password
    sed -i "s/DATABASE_PASSWORD=/DATABASE_PASSWORD=${db_password}/" .env
else
  sed -i "s/DATABASE_PASSWORD=/DATABASE_PASSWORD=$(generate_password)/" .env
fi

# Webapp settings
echo ""
echo "Настройка параметров веб-приложения..."
if ! grep -q "WEBAPP_WEBHOOK_HOST" .env; then
    echo "WEBAPP_WEBHOOK_HOST=0.0.0.0" >> .env
fi
if ! grep -q "WEBAPP_WEBHOOK_PORT" .env; then
    echo "WEBAPP_WEBHOOK_PORT=8080" >> .env
fi

echo ""
echo "=== Настройка завершена ==="
echo "Файл .env создан и настроен"
echo "Домен: ${domain}"
echo ""