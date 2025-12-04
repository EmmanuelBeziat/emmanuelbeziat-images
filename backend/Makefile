.PHONY: help migrate upgrade downgrade revision current

help:
	@echo "Available commands:"
	@echo "  make migrate          - Create initial migration"
	@echo "  make upgrade          - Apply all pending migrations"
	@echo "  make downgrade        - Revert last migration"
	@echo "  make revision MSG=... - Create new migration with message"
	@echo "  make current          - Show current database revision"
	@echo ""
	@echo "Or use: python3 -m alembic <command>"

migrate:
	python3 -m alembic revision --autogenerate -m "Initial migration"

upgrade:
	python3 -m alembic upgrade head

downgrade:
	python3 -m alembic downgrade -1

revision:
	python3 -m alembic revision --autogenerate -m "$(MSG)"

current:
	python3 -m alembic current

