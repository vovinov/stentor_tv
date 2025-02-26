DC = docker compose
STORAGES_FILE = docker_compose/storages.yaml
EXEC = docker exec -it
LOGS = docker logs
DB_CONTAINER = postgres_stentor


.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} up -d

.PHONY: storages_logs
storages_logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: storages_down
storages_down:
	${DC} -f ${STORAGES_FILE} down

