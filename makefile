all:
	docker compose down
	docker compose build
	docker compose up -d

build-no-cache:
	docker compose build --no-cache

build:
	docker compose build

run:
	docker compose up -d
kill:
	docker compose down	


migrate:
	python3 migrationts/migrate.py


