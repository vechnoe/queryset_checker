PROJECT_DIR=$(shell pwd)
VENV_DIR?=$(PROJECT_DIR)/.env
PIP?=$(VENV_DIR)/bin/pip3
PYTHON?=$(VENV_DIR)/bin/python
MANAGE?=$(PROJECT_DIR)/manage.py
NOSE?=$(VENV_DIR)/bin/nosetests
CELERY?=$(VENV_DIR)/bin/celery

.PHONY: all clean test requirements install virtualenv

all: clean virtualenv install test create_database loaddata create_admin collect_static

virtualenv:
	virtualenv -p python3 $(VENV_DIR) --no-site-packages

install: requirements

requirements:
	$(PIP) install -r $(PROJECT_DIR)/requirements.txt

celery_queries_node:
	$(CELERY) -A src worker -E -l INFO -n queries_node -Q queries

celery_data_node:
	$(CELERY) -A src worker -E -l INFO -n data_node -Q data

celery_results_node:
	$(CELERY) -A src worker -E -l INFO -n results_node -Q results

celery_flower:
	$(CELERY) flower -A  src --address=localhost --port=9999 --basic_auth=admin:12345

django_test:
	$(PYTHON) $(MANAGE) test src/apps/* --verbosity=1 --logging-level=ERROR

pep8:
	$(PROJECT_DIR)/.env/bin/flake8 --exclude '*migrations*' src

test: django_test pep8

create_database:
	$(PYTHON) manage.py migrate auth
	$(PYTHON) $(MANAGE) migrate --noinput

loaddata:
	find src/apps -name '*.json' -exec $(PYTHON) $(MANAGE) loaddata {} \;

create_admin:
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@site.com', '12345')" | $(PYTHON) $(MANAGE) shell

collect_static:
	$(PYTHON) $(MANAGE) collectstatic --no-input

run:
	$(PYTHON) $(MANAGE) runserver localhost:8000

migrations:
	$(PYTHON) $(MANAGE) makemigrations $(app)

migrate:
	$(PYTHON) $(MANAGE) migrate

shell:
	$(PYTHON) $(MANAGE) shell

clean_temp:
	find . -name '*.pyc' -delete
	rm -rf .coverage dist docs/_build htmlcov MANIFEST logs
	rm -rf $(PROJECT_DIR)/static_collected

clean_venv:
	rm -rf $(VENV_DIR)

clean: clean_temp clean_venv
