.PHONY: test
test:
	make migrate-test
	docker compose -f docker-compose.yml -f docker-compose.test.yml \
		run --rm api pytest

.PHONY: migrate-test
migrate-test:
	docker compose -f docker-compose.yml -f docker-compose.test.yml \
		run --rm api alembic upgrade head