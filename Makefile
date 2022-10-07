run:
	python -m service

renewdb:
	alembic downgrade -1
	alembic upgrade head

test:
	make renewdb
	pytest -m my --verbosity=2 --showlocals --cov=service --cov-report html

up:
	docker compose up -d

down:
	docker compose down

test2:
	make start-test-db && sleep 2
	make migrate-test-db
	export ENV="dev" && poetry run pytest -m empty tests -vv

lint:
	black service tests
	isort service tests
	pylint service

migrate-test-db:
	poetry run alembic upgrade head
