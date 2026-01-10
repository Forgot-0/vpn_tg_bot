#!/usr/bin/env bash

DC="docker compose"

set -euo pipefail

echo "=== Получение SSL сертификатов ==="

# Загрузка переменных окружения
if [ ! -f .env ]; then
    echo "Ошибка: файл .env не найден. Запустите setup-env.sh сначала"
    exit 1
fi

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
