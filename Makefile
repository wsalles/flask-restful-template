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
	@curl -X POST ${BASE_URL}/auth \
		-H 'content-type: application/json' \
		-d '{"username": "wallace", "password": "salles"}'

# PERSON-----------------------------------------------------------------------------------
create-person: check_person
	@curl -X POST ${BASE_URL}/person/${name} \
		-H 'content-type: application/json' \
		-d '{"role": "${role}", "email": "${email}"}' \
		-H 'Authorization: JWT ${token}'

update-person:
	@curl -X PUT ${BASE_URL}/person/${name} \
		-H 'content-type: application/json' \
		-d '{"role": "${role}", "email": "${email}"}' \

delete-person:
	@curl -X DELETE ${BASE_URL}/person/${name} \
		-H 'content-type: application/json'

# USERNAME --------------------------------------------------------------------------------
create-user:
	@curl -X POST ${BASE_URL}/register \
		-H 'content-type: application/json' \
		-d '{"username": "${name}", "password": "${password}", "group_id": "${group_id}"}'

update-user:
	@curl -X PUT ${BASE_URL}/register \
		-H 'content-type: application/json' \
		-d '{"username": "${name}", "password": "${password}", "group_id": "${group_id}"}'

delete-user:
	@curl -X DELETE ${BASE_URL}/register/${name} \
		-H 'content-type: application/json'

# GROUP -----------------------------------------------------------------------------------
create-group:
	@curl -X POST ${BASE_URL}/group/${name} \
		-H 'content-type: application/json'