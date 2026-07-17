.PHONY: help install install-dev venv-check pipeline run test coverage dbt-run dbt-test check docs serve clean

help:
	@echo "Available commands:"
	@echo "  make install"
	@echo "  make install-dev"
	@echo "  make venv-check"
	@echo "  make pipeline"
	@echo "  make test"
	@echo "  make coverage"
	@echo "  make dbt-run"
	@echo "  make dbt-test"
	@echo "  make check"
	@echo "  make docs"
	@echo "  make serve"
	@echo "  make clean"

install:
	python -m pip install -r requirements.txt

install-dev:
	python -m pip install -r requirements-dev.txt

venv-check:
	@python --version
	@which python
	@which pip
	@which pytest

pipeline:
	python run_pipeline.py

test:
	python -m pytest

coverage:
	python -m pytest --cov=src

dbt-run:
	cd dbt && dbt run

dbt-test:
	cd dbt && dbt test

check: test dbt-test
	@echo "All checks passed."

docs:
	cd dbt && dbt docs generate

serve:
	cd dbt && dbt docs serve

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf dbt/target