check-install-%:
	$(eval REQ := $(shell which $* ))
	@if [ "${token}" = "" ]; then \
		echo "${WARNING}Please, consider doing: \n${BOLD_WARNING}make setup \n \
		      ${NC}${WARNING}\nOr just do it: \n${BOLD_WARNING}pip install $*"; \
		exit 1; \
	 fi ||:

check_token:
	@if [ -z "${token}" ]; then \
  	echo "${WARNING}You need to enter a token. \
  	     \n(e.g: make person ${BOLD_WARNING}token=XXXXXX${NC}${WARNING} name=noname career=havent email=test@pt.br)${NC}"; \
	exit 1; fi ||:

check_person:
	@if [ -z "${name}" ] || [ -z "${career}" ] || [ -z "${email}" ]; then \
  	echo "${WARNING}You need to enter your name, career and email. \
  		 \n(e.g: make person token=XXXXXX ${BOLD_WARNING}name=noname career=havent email=test@pt.br)${NC}"; \
	exit 1; fi ||: