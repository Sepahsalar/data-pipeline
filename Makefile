.PHONY: help install install-dev venv-check pipeline reset-data run test coverage dbt-run dbt-test check docs serve clean

help:
	@echo "Available commands:"
	@echo "  make install"
	@echo "  make install-dev"
	@echo "  make venv-check"
	@echo "  make pipeline"
	@echo "  make reset-data"
	@echo "  make test"
	@echo "  make coverage"
	@echo "  make dbt-run"
	@echo "  make dbt-test"
	@echo "  make check"
	@echo "  make docs"
	@echo "  make serve"
	@echo "  make clean"

install:
	python -m pip install -r requirements/etl.txt

install-dev:
	python -m pip install -r requirements/dev.txt

venv-check:
	@python --version
	@which python
	@which pip
	@which pytest

pipeline: reset-data
	python run_pipeline.py

reset-data:
	rm -f data/users_*

test:
	python -m pytest

coverage:
	python -m pytest --cov=src

dbt-run:
	cd dbt && dbt run --profiles-dir .

dbt-test:
	cd dbt && dbt test --profiles-dir .

check: test dbt-test
	@echo "All checks passed."

docs:
	cd dbt && dbt docs generate --profiles-dir .

serve:
	cd dbt && dbt docs serve --profiles-dir .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf dbt/target
	rm -rf dbt/dbt_packages
	rm -rf dbt/logs