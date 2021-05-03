.PHONY: setup run
-include makefiles/*.mk

# Main variables
BASE_URL := http://localhost:5000
# JWT
jwt_user := wallace
jwt_pass := salles

# ENVIRONMENT -----------------------------------------------------------------------------
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

# JWT: /AUTH ------------------------------------------------------------------------------
token:
	@curl -X POST ${BASE_URL}/auth \
		-H 'content-type: application/json' \
		-d '{"username": "${jwt_user}", "password": "${jwt_pass}"}'

# PERSON ----------------------------------------------------------------------------------
create-person: check_person
	@curl -X POST ${BASE_URL}/person/${name} \
		-H 'content-type: application/json' \
		-d '{"role": "${role}", "email": "${email}"}' \
		-H 'Authorization: JWT ${token}'

update-person: check_person
	@curl -X PUT ${BASE_URL}/person/${name} \
		-H 'content-type: application/json' \
		-d '{"role": "${role}", "email": "${email}"}' \

delete-person:
	@curl -X DELETE ${BASE_URL}/person/${name} \
		-H 'content-type: application/json'

# USERNAME --------------------------------------------------------------------------------
create-user: check_user
	@curl -X POST ${BASE_URL}/register \
		-H 'content-type: application/json' \
		-d '{"username": "${name}", "password": "${password}", "group_id": "${group_id}"}'

update-user: check_user
	@curl -X PUT ${BASE_URL}/register \
		-H 'content-type: application/json' \
		-d '{"username": "${name}", "password": "${password}", "group_id": "${group_id}"}'

delete-user:
	@curl -X DELETE ${BASE_URL}/register/${name} \
		-H 'content-type: application/json'

# GROUP -----------------------------------------------------------------------------------
create-group: check_group
	@curl -X POST ${BASE_URL}/group/${name} \
		-H 'content-type: application/json'