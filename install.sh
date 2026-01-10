#!/usr/bin/env bash

set -euo pipefail

echo "=== Установка зависимостей на сервер ==="

# Обновление системы
echo "Обновление системы..."
sudo apt-get update -y
sudo apt-get upgrade -y


# Установка Docker Compose
echo "Установка Docker Compose..."
if ! command -v docker compose &> /dev/null; then
    sudo apt install ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt update
    sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
else
    echo "Docker Compose уже установлен"
fi

# Создание Docker network
echo "Создание Docker network..."
docker network create app-network 2>/dev/null || echo "Network app-network уже существует"

# Установка дополнительных утилит
echo "Установка дополнительных утилит..."
sudo apt-get install -y git curl wget nano

echo "=== Установка завершена ==="
echo "ВНИМАНИЕ: Если Docker был только что установлен, выполните:"
echo "  newgrp docker"
echo "или перелогиньтесь для применения изменений в группах"


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
sed -i "s/VPN_HELP_ACCOUNT=/VPN_HELP_ACCOUNT=${vpn_help}/" .env


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


source .env

if [ -z "$DOMAIN" ]; then
    echo "Ошибка: DOMAIN не установлен в .env"
    exit 1
fi

echo "Домен: $DOMAIN"


echo ""
echo "Проверка DNS записей..."
echo "Проверяем $DOMAIN"
domain_ip=$(dig +short $DOMAIN | tail -n1)
api_domain_ip=$(dig +short api.$DOMAIN | tail -n1)
server_ip=$(curl -s ifconfig.me)

echo "IP сервера: $server_ip"
echo "IP домена $DOMAIN: $domain_ip"
echo "IP домена api.$DOMAIN: $api_domain_ip"

if [ "$domain_ip" != "$server_ip" ] || [ "$api_domain_ip" != "$server_ip" ]; then
    echo ""
    echo "ВНИМАНИЕ: DNS записи не совпадают с IP сервера!"
    echo "Убедитесь что A-записи для $DOMAIN и api.$DOMAIN указывают на $server_ip"
    read -p "Продолжить? (y/n): " continue
    if [ "$continue" != "y" ]; then
        exit 1
    fi
fi

sed -i 's|      # - ./nginx/start/:/etc/nginx/templates/|      - ./nginx/start/:/etc/nginx/templates/|' docker-compose.prod.yml
sed -i 's|      - ./nginx/templates/:/etc/nginx/templates/|      # - ./nginx/templates/:/etc/nginx/templates/|' docker-compose.prod.yml

echo "Сборка ..."
docker compose -f docker-compose.prod.yml --env-file .env up -d
echo "Ожидание завершения сборки..."
sleep 10


echo ""
echo "Получение сертификатов для $DOMAIN..."
read -p "Введите вашу почту: " email
docker compose -f docker-compose.prod.yml run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email ${email} \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN

docker compose -f docker-compose.prod.yml run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email ${email} \
    --agree-tos \
    --no-eff-email \
    -d api.$DOMAIN

docker compose -f docker-compose.prod.yml down

sed -i 's|      - ./nginx/start/:/etc/nginx/templates/|      # - ./nginx/start/:/etc/nginx/templates/|' docker-compose.prod.yml
sed -i 's|      # - ./nginx/templates/:/etc/nginx/templates/|      - ./nginx/templates/:/etc/nginx/templates/|' docker-compose.prod.yml


if [ ! -f "nginx/ssl/live/$DOMAIN/fullchain.pem" ] || [ ! -f "nginx/ssl/live/api.$DOMAIN/fullchain.pem" ]; then
    echo ""
    echo "ОШИБКА: Не удалось получить сертификаты!"
    echo "Проверьте DNS записи и доступность портов 80 и 443"
    exit 1
fi

docker compose -f docker-compose.yml -f docker-compose.prod.yml -f docker-compose.monitoring.yml --env-file .env up -d
