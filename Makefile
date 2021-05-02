.PHONY: setup run
-include makefiles/*.mk

# Main variables
BASE_URL := http://localhost:5000

setup:
	@echo "${SETUP}"
	@pip install -r requirements.txt

run: check-install-flask check-install-uwsgi
	@echo "${RUNNING}"
	@uwsgi --ini uwsgi.ini

dev:
	@FLASK_ENV=development flask run

routes:
	@flask routes

token:
	@curl -X POST ${BASE_URL}/auth -H 'content-type: application/json' -d '{"username": "wallace", "password": "salles"}'

person: check_token check_person
	@curl -X POST ${BASE_URL}/people/${name} \
		-H 'content-type: application/json' \
		-H 'Authorization: JWT ${token}' \
		-d '{"career": "${career}", "email": "${email}"}'
