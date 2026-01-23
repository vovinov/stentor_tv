MANAGE_PY = py manage.py


.PHONY: runserver
runserver: 
	${MANAGE_PY} runserver

.PHONY: mi
mi: 
	${MANAGE_PY} makemigrations && ${MANAGE_PY} migrate

	