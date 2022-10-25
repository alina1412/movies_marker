run:
	poetry run python -m service

renew-sync:
	alembic -c alembic_s.ini downgrade -1
	alembic -c alembic_s.ini upgrade head

test-sync:
	make renew-sync
	pytest -m my --verbosity=2 --showlocals --cov=service --cov-report html

renew-async:
	alembic -c alembic_as.ini downgrade -1
	alembic -c alembic_as.ini upgrade head

test-async:
	make renew-async
	pytest -m my --verbosity=2 --showlocals --cov=service --cov-report html

async-alembic-init:
	alembic init -t async async_migrations
	alembic -c alembic_as.ini revision --autogenerate -m "asyncinitial"

async-alembic-up:
	alembic -c alembic_as.ini upgrade head

async-alembic-down:
	alembic -c alembic_as.ini downgrade -1

up:
	docker compose up -d

down:
	docker compose down

test2-example:
	make start-test-db && sleep 2
	make migrate-test-db
	export ENV="dev" && poetry run pytest -m empty tests -vv

lint:
	black service tests
	isort service tests
	pylint service

req:
	poetry export -f requirements.txt --without-hashes --with dev --output ./service/requirements.txt
