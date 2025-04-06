DC = docker compose
STORAGES_FILE = docker_compose/storages.yaml
EXEC = docker exec -it
DB_CONTAINER = postgresdb
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
APP_CONTAINER = workly-app
BROKER_FILE = docker_compose/broker.yaml
TELEGRAM_BOT_FILE = docker_compose/tg_bot.yaml



.PHONY: tg_bot
bot:
	${DC} -f ${TELEGRAM_BOT_FILE} ${ENV} up -d


.PHONY: broker
broker:
	${DC} -f ${BROKER_FILE} ${ENV} up -d

.PHONY: broker-down
broker-down:
	${DC} -f $(BROKER_FILE) down

.PHONY: broker-logs
broker-logs:
	${LOGS} ${BROKER_FILE} -f


.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up -d


.PHONY: storages-down
storages-down:
	${DC} -f $(STORAGES_FILE) down


.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f


.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${BROKER_FILE} -f ${TELEGRAM_BOT_FILE} ${ENV} up --build -d


.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f


.PHONY: app-down
app-down:
	${DC} -f $(STORAGES_FILE) -f ${BROKER_FILE} -f ${APP_FILE} -f ${TELEGRAM_BOT_FILE} down


.PHONY: alembic-revision
alembic-revision:
	${EXEC} ${APP_CONTAINER} alembic revision --autogenerate


.PHONY: alembic-upgrade
alembic-upgrade:
	${EXEC} ${APP_CONTAINER} alembic upgrade head


.PHONY: run-test
run-test:
	${EXEC} ${APP_CONTAINER} env PYTHONPATH=/app pytest -s -v