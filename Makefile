alembic_up = make async-alembic-up

ifdef OS
	docker_up = docker compose up -d
	docker_down = docker compose down --volumes
else
	docker_up = sudo docker-compose up -d
	docker_down = sudo docker-compose down
endif

up:
	$(docker_up) 
	$(alembic_up)

down:
	$(docker_down)

run:
	poetry run python -m service

renew-sync:
	poetry run alembic -c alembic_s.ini downgrade -1
	poetry run alembic -c alembic_s.ini upgrade head

test-sync:
	make renew-sync
	poetry run pytest -m my --verbosity=2 --showlocals --cov=service --cov-report html

renew-async:
	poetry run alembic -c alembic_as.ini downgrade -1
	poetry run alembic -c alembic_as.ini upgrade head

test:
	make renew-async
	poetry run pytest -m my --verbosity=2 --showlocals

async-alembic-init:
	poetry run alembic init -t async async_migrations
	poetry run alembic -c alembic_as.ini revision --autogenerate -m "async_initial"

async-alembic-up:
	poetry run alembic -c alembic_as.ini upgrade head

async-alembic-down:
	poetry run alembic -c alembic_as.ini downgrade -1

lint:
	poetry run isort service tests
	poetry run black service tests
	poetry run pylint service

req:
	poetry export -f requirements.txt --without-hashes --with dev --output ./service/requirements.txt
