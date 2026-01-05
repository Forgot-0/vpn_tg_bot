DC = docker compose
EXEC = docker exec -it
BOT_APP = docker-compose.yml
WEB_SERVER = docker-compose.prod.yml
ENV = --env-file .env
APP_CONTAINER = app


.PHONY: up_local
up_local:
	${DC} ${ENV} up -d --build

.PHONY: down_local
down_local:
	${DC} ${ENV} down

.PHONY: certbot
certbot:
	${DC} -f ${BOT_APP} -f ${WEB_SERVER} ${ENV} run --rm certbot certonly --webroot --webroot-path=/var/www/certbot -d example.com -d api.example.com

.PHONY: certbot_wildcat
certbot:
	${DC} -f ${BOT_APP} -f ${WEB_SERVER} ${ENV} run --rm certbot certonly --manual --preferred-challenges=dns --webroot --webroot-path=/var/www/certbot -d example.com -d *.example.com

.PHONY: app_prod
app_prod:
	${DC} -f ${BOT_APP} -f ${WEB_SERVER} ${ENV} up -d --build

.PHONY: up_webhook
up_webhook:
	ngrok http --url=probably-stable-tortoise.ngrok-free.app 8080

