check-install-%:
	$(eval REQ := $(shell which $* ))
	@if [ "${REQ}" = "" ]; then \
		echo "${WARNING}Please, consider doing: \n${BOLD_WARNING}make setup \n \
		      ${NC}${WARNING}\nOr just do it: \n${BOLD_WARNING}pip install $*"; \
		exit 1; \
	 fi ||:

check_token:
	@if [ -z "${token}" ]; then \
  	echo "${WARNING}You need to enter a token. \
  	     \n(e.g: make person ${BOLD_WARNING}token=XXXXXX${NC}${WARNING} name=noname role=havent email=test@pt.br)${NC}"; \
	exit 1; fi ||:

check_person:
	@if [ -z "${name}" ] || [ -z "${role}" ] || [ -z "${email}" ]; then \
  	echo "${WARNING}You need to enter your name, role and email. \
  		 \n(e.g: ${BOLD_WARNING}name=noname role=havent email=test@pt.br)${NC}"; \
	exit 1; fi ||:

check_user:
	@if [ -z "${name}" ] || [ -z "${password}" ] || [ -z "${group_id}" ]; then \
  	echo "${WARNING}You need to enter the username, password and group_id. \
  		 \n(e.g: ${BOLD_WARNING}name=wallace password=salles group_id=1)${NC}"; \
	exit 1; fi ||:

check_group:
	@if [ -z "${name}" ]; then \
  	echo "${WARNING}You need to enter the group name. \
  		 \n(e.g: ${BOLD_WARNING}name=admin)${NC}"; \
	exit 1; fi ||: