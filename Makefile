DC = docker compose
BOT_APP = docker_compose/app.yaml
STORAGE = docker_compose/storage.yaml
WEB_SERVER = docker_compose/webserver.yaml
ENV = --env-file .env


.PHONY: bot_up
bot_up:
	${DC} -f ${BOT_APP} ${ENV} up -d --build

.PHONY: bot_down
bot_down:
	${DC} -f ${BOT_APP} ${ENV} down

.PHONY: app_up
app_up:
	${DC} -f ${WEB_SERVER} -f ${BOT_APP} ${ENV} up -d --build

.PHONY: storage_up
storage_up:
	${DC} -f ${STORAGE} ${ENV} up -d --build

.PHONY: storage_down
storage_down:
	${DC} -f ${STORAGE} ${ENV} down

.PHONY: app_down
app_down:
	${DC} -f ${WEB_SERVER} -f ${BOT_APP} -f ${STORAGE} ${ENV} down