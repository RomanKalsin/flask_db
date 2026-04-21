include .env
export

build:
	psql -a -d $(DATABASE_URL) -f ./db/init.sql

start_flask:
	uv run flask --app src.app --debug run --port 8000

start_gunicorn:
	uv run gunicorn

ruff_check:
	uv run ruff check
