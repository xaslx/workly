DC = docker compose
STORAGES_FILE = docker_compose/storages.yaml
EXEC = docker exec -it
DB_CONTAINER = postgresdb
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
APP_CONTAINER = workly-app

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
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} ${ENV} up --build -d


.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f


.PHONY: app-down
app-down:
	${DC} -f $(STORAGES_FILE) -f ${APP_FILE} down


.PHONY: alembic-revision
alembic-revision:
	${EXEC} ${APP_CONTAINER} alembic revision --autogenerate


.PHONY: alembic-upgrade
alembic-upgrade:
	${EXEC} ${APP_CONTAINER} alembic upgrade head


.PHONY: run-test
run-test:
	${EXEC} ${APP_CONTAINER} env PYTHONPATH=/app pytest -s -v