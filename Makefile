.PHONY: help install pipeline run test docs serve clean

help:
	@echo "Available commands:"
	@echo "  make install"
	@echo "  make pipeline"
	@echo "  make dbt-run"
	@echo "  make dbt-test"
	@echo "  make docs"
	@echo "  make serve"
	@echo "  make clean"

install:
	pip install -r requirements.txt

pipeline:
	python run_pipeline.py

dbt-run:
	cd dbt && dbt run

dbt-test:
	cd dbt && dbt test

docs:
	cd dbt && dbt docs generate

serve:
	cd dbt && dbt docs serve

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf dbt/target