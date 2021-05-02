# Customizing your output
CODE_CHANGE="\\033["
WARNING := $(shell echo ${CODE_CHANGE}'33;5m')
BOLD_WARNING := $(shell echo ${CODE_CHANGE}'33;1m')
RUNNING := $(shell echo ${CODE_CHANGE}'32;5m')
SETUP := $(shell echo ${CODE_CHANGE}'36;4m')
NC := $(shell echo ${CODE_CHANGE}'0m')
