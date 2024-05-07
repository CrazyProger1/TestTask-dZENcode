.PHONY: install
install:
	poetry install

.PHONY: migrations
migrations:
	poetry run python manage.py makemigrations

.PHONY: migrate
migrate: migrations
	poetry run python manage.py migrate

.PHONY: run-server
run-server:
	poetry run python manage.py runserver

.PHONY: admin
admin:
	poetry run python manage.py createsuperuser

.PHONY: test-admin
test-admin:
	poetry run python manage.py createsuperuser --username admin --email admin@admin.com

.PHONY: update
update: install migrate;


.PHONY: code-check
code-check:
	poetry run python -m black .
	poetry run python -m mypy .

.PHONY: test
test:
	poetry run python manage.py test


.PHONY: coverage-report
coverage-report:
	poetry run coverage run manage.py test
	poetry run coverage report -m