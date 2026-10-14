CURR_DIR	:=	$(shell pwd)
VENV_DIR	:=	$(CURR_DIR)/.venv
PYTHON	:=	$(VENV_DIR)/bin/python
UTIL_PYCACHE	:=	"$(CURR_DIR)/src/utils/__pycache__"

CORE_CONFIG_FILE	:=	"$(CURR_DIR)/src/config/settings.ini"
DEV_CONFIG_FILE	:=	"$(CURR_DIR)/src/config/settings-dev.ini"

install:
	@bash install.sh

start:
	@CORE_CONFIG_FILE=$(CORE_CONFIG_FILE) \
	$(PYTHON) src/worker.py

dev:
	@CORE_CONFIG_FILE=$(DEV_CONFIG_FILE) \
	$(PYTHON) src/worker.py

stage:
	@CORE_CONFIG_FILE=$(CORE_CONFIG_FILE) \
	$(PYTHON) src/worker.py

clean:
	@echo -n "Cleaning... "
	@$(RM) -r $(UTIL_PYCACHE)
	@echo "\33[32;5mOK\033[m" || echo "\33[31;5mERROR\33[m"

.PHONY: install start dev stage clean
