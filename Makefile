.DELETE_ON_ERROR:
.PHONY: FORCE
.PRECIOUS:
.SUFFIXES:

VE_DIR=venv

# => create a Python3 venv with all the dependencies
.PHONY: install
install:
	python3 -m venv ${VE_DIR}; \
	source ${VE_DIR}/bin/activate; \
	pip install -r requirements.txt; \

.PHONY: setup
setup:
	source ${VE_DIR}/bin/activate; \
	cd marriagesaver; \
	python manage.py migrate; \
	python manage.py createsuperuser; \

.PHONY: runserver
runserver:
	source ${VE_DIR}/bin/activate; \
	cd marriagesaver; \
	python manage.py runserver